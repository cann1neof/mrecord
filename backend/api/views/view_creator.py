import json
import random
import string

from Crypto.Hash import MD5
from django.db.models import ObjectDoesNotExist

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Record, User, Doctor, Hospital
from api.models import Moderator, KeysToken, UnregisteredRecord
from api.serializer import ChildRecordSerializer

from serv.MRDApi import Cryptographer

class Creator(APIView):
    cryp = Cryptographer()

    def post(self, req, meta=''):
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.data.get('token'))
        data = req.data.get('data')
        if token.is_valid():
            print(meta)
            if meta == 'd':
                print('yay1')
                return self._create_doctor(token.user, data)
            elif meta == 'm':
                return self._create_moderator(token.user, data)
            elif meta == 'h':
                return self._create_hospital(token.user, data)
            elif meta == 'c':
                return self._create_child_record(token.user, data)
            else:
                return Response(status=400, data={'error': 'lul'})
        else:
            return Response(status=401)
            
    def delete(self, req, meta=''):
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.data.get('token'))
        if token.is_valid():
            try:
                usr = User.objects.get(username=req.data.get('username'))
            except ObjectDoesNotExist:
                return Response(status=404, data="noSuchUser")
            try:
                doc = Doctor.objects.get(user=usr)
            except ObjectDoesNotExist:
                return Response(status=404, data="noSuchDoctor")
            
            doc.delete()
            return Response(status=200)
        return Response(status=403)

    def _create_child_record(self, user, data):
        if data['id_exists']:
            try:
                empty_record = UnregisteredRecord.bjects.get(
                    serial_number=data['serial_number'])
            except ObjectDoesNotExist:
                return Response(status=412)

            if empty_record.code == data['code']:
                data['serial_number'] = data['serial_number']
                empty_record.delete()
            else:
                return Response(status=403)
        else:
            serial_number = ''.join(
                random.choice(
                    string.ascii_uppercase +
                    string.digits) for i in range(8))
            data['serial_number'] = serial_number

        child_rec_ser = ChildRecordSerializer(data=data)
        if child_rec_ser.is_valid():
            child_rec = child_rec_ser.save()

            child_rec.parent = user
            child_rec.save()
            try:
                par_record = Record.objects.get(owner=user)
            except ObjectDoesNotExist:
                return Response(status=404)

            json_decoder = json.JSONDecoder()
            children = json_decoder.decode(par_record.children)
            children.append({
                'name': f'{child_rec.last_name} {child_rec.first_name} {child_rec.second_name}',
                'serial_number': child_rec.serial_number,
                'birthday': child_rec.birthday.strftime('%d.%m.%Y')
            })
            par_record.children = json.dumps(
                children, separators=(
                    ',', ':'), ensure_ascii=False)
            par_record.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def _create_doctor(self, user, data):
        if user.is_moderator or user.is_staff or user.is_superuser:
            instance_name = data['instance']
            print('yay2')
            try:
                moder = Moderator.objects.get(user=user)
                hospital = moder.hospital
                instance = User.objects.get(username=instance_name)
            except ObjectDoesNotExist:
                return Response(status=400)

            my_hash = MD5.new()
            timestamp = self.cryp.timestamp()
            my_hash.update(str(timestamp).encode())

            doc = Doctor(
                user=instance,
                hospital=hospital,
                code=my_hash.hexdigest()
            )
            doc.save()
            instance.is_doctor = True
            instance.save()

            return Response(status=201)
        else:
            return Response(status=403)

    def _create_moderator(self, user, data):
        if user.is_staff or user.is_superuser:
            instance_name = data['instance']
            hospital_code = data['hc']
            try:
                hospital = Hospital.objects.get(code=hospital_code)
                instance = User.objects.get(username=instance_name)
            except ObjectDoesNotExist:
                return Response(status=400)

            mod = Moderator(
                user=instance,
                hospital=hospital,
            )
            mod.save()
            instance.is_moderator = True
            instance.save()

            return Response(status=201)
        else:
            return Response(status=403)

    def _create_hospital(self, user, data):
        if user.is_superuser:
            region = data['region']
            country = data['country']
            city = data['city']
            street = data['street']
            geo_data = data['geo_data']
            post_index = data['post_index']
            name = data['name']
            additional = data['additional']

            my_hash = MD5.new()
            timestamp = self.cryp.timestamp()
            my_hash.update(str(timestamp).encode())

            hos = Hospital(
                region=region,
                country=country,
                city=city,
                street=street,
                geo_data=geo_data,
                post_index=post_index,
                name=name,
                additional=additional,
                code=my_hash.hexdigest()
            )
            hos.save()
            return Response(status=201)
        else:
            return Response(status=403)
