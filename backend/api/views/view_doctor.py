from json import JSONDecoder, dumps

from django.db.models import ObjectDoesNotExist

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Record, Doctor, KeysToken, Event
from api.serializer import RecordSerializer


class DoctorApi(APIView):
    def put(self, req):
        print(req.data)
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.data.get('token'))
        if token.is_valid() and token.user.is_doctor:
            try:
                record = Record.objects.get(serial_number=req.data.get('id'))
            except ObjectDoesNotExist:
                return Response(status=400)
            decoder = JSONDecoder()
            raw_record_data = decoder.decode(req.data.get('rec'))
            record_data = {}
            try:
                record_data['illnesses'] = dumps(raw_record_data['illnesses'], separators=(',',':'))
            except KeyError:
                pass
            try:
                record_data['recipes'] = dumps(raw_record_data['recepies'], separators=(',',':'))
            except KeyError:
                pass
            rec_ser = RecordSerializer(
                instance=record, data=record_data, partial=True)
            if rec_ser.is_valid():
                print('yay')
                rec_ser.save()
                token.update_activity()
                return Response(status=200)
            else:
                print(rec_ser.errors)
                return Response(status=400)

        elif not token.user.is_doctor:
            return Response(status=403)
        else:
            return Response(status=401)

    def post(self, req):
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.data.get('token'))
        print(req.data)
        if token.is_valid() and token.user.is_doctor:
            result = req.data.get('res')
            try:
                print(req.data.get('id'))
                record = Record.objects.get(serial_number=req.data.get('id'))
                print(record)
            except ObjectDoesNotExist:
                return Response(status=400)

            json_decoder = JSONDecoder()
            events = json_decoder.decode(str(record.hospitals), )
            doctor = Doctor.objects.get(user=token.user)

            event = Event(
                doctor=doctor,
                user=record.owner,
                result=result
            )
            event.save()

            events.append({
                'address': doctor.hospital.get_obj(),
                'date': event.date.strftime('%d.%m.%Y %H:%M'),
                'doctor': str(doctor),
                'result': result
            })
            hospitalz = (
                dumps(
                    events,
                    separators=(',', ':'),
                    ensure_ascii=False)
                ).replace("'", '"')
            record.hospitals = hospitalz
            record.save()
            token.update_activity()
            return Response(status=201)

        elif not token.user.is_doctor:
            return Response(status=403)
        else:
            return Response(status=401)
