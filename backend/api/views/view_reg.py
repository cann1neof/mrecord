import random
import string

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer import UserSerializer, RecordSerializer
from api.models import UnregisteredRecord, User
from serv.MRDApi import Cryptographer
from serv.settings import DEBUG

class Registration(APIView):
    cryp = Cryptographer()

    def get(self, req):
        if DEBUG:
            print(req)
        code = [
            random.choice(
                string.digits +
                string.ascii_letters) for i in range(0, 16)]
        salt = ''.join(code)
        return Response(data={'salt': salt}, status=200)

    def post(self, req):
        registration_type = req.data.get('id_exists')
        user_data = req.data.get('usr')
        record_data = req.data.get('rec')

        if registration_type:
            empty_record_data = req.data.get('mrd')
            serial_number = empty_record_data['id']
            unreg_rec = UnregisteredRecord.objects.get(
                serial_number=serial_number)
            if not unreg_rec.code == empty_record_data['code']:
                return Response(status=403)
            else:
                record_data['serial_number'] = unreg_rec.serial_number
                unreg_rec.delete()
        else:
            code = [
                random.choice(
                    string.ascii_letters +
                    string.digits) for i in range(0, 6)]
            record_data['serial_number'] = ''.join(code)

        if len(user_data['password'].split('$')) == 2:
            user_ser = UserSerializer(data=user_data)
            record_ser = RecordSerializer(data=record_data)
        else:
            return Response(status=400)

        if user_ser.is_valid() and record_ser.is_valid():
            success = self._unique_check(user_data)
            if success == None:
                user = user_ser.save()
                record = record_ser.save()
                record.owner_id = user.id
                record.save()
                token = self.cryp.generate_token(user)
                token.login()
                return Response(status=200, data={'token': token.token})
            return Response(status=208, data={'error': success})
        return Response(status=400)

    def _unique_check(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(email=data['email'])
            except ObjectDoesNotExist: 
                try:
                    user = User.objects.get(telephone=data['telephone'])
                except ObjectDoesNotExist:
                    return None
                else:
                    return 'telephoneError'
            else:
                return 'emailError'
        else:
            return 'userNameError'

