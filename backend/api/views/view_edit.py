from json import JSONDecoder, dumps

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import ObjectDoesNotExist

from api.models import Record, KeysToken, ChildRecord, User, UnregisteredRecord
from api.serializer import RecordSerializer, UserSerializer, ChildRecordSerializer

from serv.MRDApi import Cryptographer, NotValid

class Editor(APIView):
    cryp = Cryptographer()

    def put(self, req):
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.data['token'])
        user = token.user
        if token.is_valid():
            token.update_activity()
            user_data = req.data['usr']
            errors = [None, None]
            try:
                errors[0] = self._update_user_data(user_data, user)
            except NotValid:
                return Response(status=400, data="lel")
            if errors[0] != None:
                return Response(status=400, data=errors[0])

            record_data = req.data['rec']
            try:
                errors[1] = self._update_record_data(record_data, user)
            except NotValid:
                return Response(status=400)
            if errors[1] != None:
                return Response(status=400, data=errors[1])

            return Response(status=200)
        else:
            return Response(status=401)

    def _update_user_data(self, user_data, user):
        unique_status, errors = self._unique_user_creds(user_data, user)

        if unique_status:
            usr_ser = UserSerializer(instance=user, data=user_data, partial=True)
            if usr_ser.is_valid():
                usr_ser.save()
            else:
                raise NotValid
        if errors == None:
            return None
        return errors

    def _update_record_data(self, record_data, user):
        record = get_object_or_404(Record.objects.all(), owner=user)
        unique_status, errors = self._unique_record_creds(record_data, record)
        if unique_status:
            rec_ser = RecordSerializer(
                instance=record,
                data=record_data,
                partial=True)
            if rec_ser.is_valid():
                rec_ser.save()
            else:
                raise NotValid
        if errors == None:
            return None
        return errors

    def  _unique_record_creds(self, record_data, record_instance):
        record = None
        errors = []
        if 'serial_number' in record_data.keys():
            try:
                record = Record.objects.get(serial_number=record_data['serial_number'])
            except ObjectDoesNotExist:
                record = None
            if record:
                errors.append('serialNumberError')

            try:
                snum = record_data['serial_number']
                unreg_rec = UnregisteredRecord.objects.get(serial_number=snum)
            except ObjectDoesNotExist:
                errors.append('noSuchRecord')
                unreg_rec = None

            if unreg_rec and unreg_rec.code == record_data['code']:
                if not record or record == record_instance:
                    record_instance.serial_number = record_data['serial_number']
                    record_instance.save()
                    unreg_rec.delete()
                    return True, None
            return False, errors
        return True, None

    def _unique_user_creds(self, user_data, user_instance):
        user = None
        errors = []
        if 'username' in user_data.keys():
            try:
                user = User.objects.get(username=user_data['username'])
            except ObjectDoesNotExist:
                user = None
            if user:
                errors.append('usernameError')
        if 'email' in user_data.keys():
            try:
                user = User.objects.get(email=user_data['email'])
            except ObjectDoesNotExist:
                user = None
            if user:
                errors.append('emailError')
        if 'telephone' in user_data.keys():
            try:
                user = User.objects.get(telephone=user_data['telephone'])
            except ObjectDoesNotExist:
                user = None
            if user:
                errors.append('phoneError')
        if 'email' in user_data.keys() or 'username' in user_data.keys() or 'telephone' in user_data.keys():
            if user != user_instance and errors:
                return False, errors
            elif not user or user == user_instance:
                return True, None
        return True, None

class ChildEditor(APIView):
    def put(self, req):
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.data['token'])
        user = token.user
        child_rec = get_object_or_404(
            ChildRecord.objects.all(),
            serial_number=req.data['id'])
        if token.is_valid() and child_rec.parent == user:
            data = req.data['data']
            rec = ChildRecordSerializer(
                instance=child_rec, data=data, partial=True)
            if rec.is_valid():
                rec.save()

            parent_record = Record.objects.get(owner=user)

            json_decoder = JSONDecoder()
            children = json_decoder.decode(parent_record.children)

            if rec.is_valid() and (
                    data['first_name'] or data['last_name'] or data['second_name']):
                for each in children:
                    if each['serial_number'] == req.data['id']:
                        tmp = f'{rec.data["last_name"]} '
                        tmp += f'{rec.data["first_name"]} '
                        tmp += f'{rec.data["second_name"]}'
                        each['name'] = tmp
                parent_record.children = dumps(
                    children, separators=(
                        ',', ':'), ensure_ascii=False)
                parent_record.save()

            token.update_activity()
            return Response(status=200)
        else:
            return Response(status=403)
