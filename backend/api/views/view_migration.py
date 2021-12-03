import random
import string
import json

from Crypto.Hash import SHA256
from django.db.models import ObjectDoesNotExist

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Record, User, ChildRecord, UnregisteredRecord
from api.models import KeysToken, MigrationToken

from serv.MRDApi import Cryptographer


class ChildMigration(APIView):
    def post(self, req):
        migration_token = get_object_or_404(
            MigrationToken.objects.all(),
            token=req.data.get('token'))
        password = req.data.get('password')
        username = req.data.get('username')
        email = req.data.get('email')
        contacts = req.data.get('contacts')
        telephone = req.data.get('telephone')

        child = migration_token.user

        if migration_token.is_valid():
            if req.data.get('id_exists'):
                serial_number = req.data.get('id')
                code = req.data.get('code')
                try:
                    urec = UnregisteredRecord.objects.get(
                        serial_number=serial_number)
                except ObjectDoesNotExist:
                    return Response(status=404)

                if not urec.code == code:
                    return Response(status=403)
            else:
                if len(child.serial_number) == 8:
                    serial_number = ''.join(
                        [random.choice(string.ascii_letters + string.digits) for i in range(0, 6)])
                else:
                    serial_number = child.serial_number
            try:
                temp_user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                temp_user = None

            self._delete_this_from_parent(migration_token)

            if len(password.split('$')) == 2 and temp_user is None:
                user = User(
                    password=password,
                    username=username,
                    first_name=child.first_name,
                    last_name=child.last_name,
                    second_name=child.second_name,
                    email=email,
                    telephone=telephone
                )
                user.save()

                record = Record(
                    serial_number=serial_number,
                    insurance_number=child.insurance_number,
                    illnesses=child.illnesses,
                    contacts=contacts,
                    hospitals=child.hospitals,
                    recipes=child.recipes,
                    blood_type=child.blood_type,
                    children='[]',
                    owner=user
                )
                record.save()
                child.delete()
                migration_token.delete()

                return Response(status=201)
            else:
                return Response(status=400)
        else:
            return Response(status=401)

    def _delete_this_from_parent(self, token):
        child = token.user
        parent = Record.objects.get(owner=token.parent)
        json_decoder = json.JSONDecoder()
        children = json_decoder.decode(parent.children)
        for each in children:
            if each['serial_number'] == child.serial_number:
                children.remove(each)
        parent.children = json.dumps(
            children, separators=(
                ',', ':'), ensure_ascii=False)
        parent.save()


class StartChildMigration(APIView):
    cryp = Cryptographer()

    def post(self, req):
        par_token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.data.get('token'))
        try:
            child = ChildRecord.objects.get(serial_number=req.data.get('id'))
        except ObjectDoesNotExist:
            return Response(status=400)

        if par_token.is_valid() and child.parent == par_token.user:
            timestamp = str(self.cryp.timestamp())
            my_hash = SHA256.new()
            my_hash.update(timestamp.encode())
            token = my_hash.hexdigest()

            mig_token = MigrationToken(
                token=token,
                user=child,
                parent=par_token.user
            )
            mig_token.save()

            par_token.update_activity()
            return Response(status=200, data={'token': token})

        elif not child.parent == token.user:
            return Response(status=403)
        else:
            return Response(status=401)
