from json import JSONDecoder
from abc import ABCMeta, abstractmethod
from django.db.models import ObjectDoesNotExist

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from serv.MRDApi import Cryptographer, NoUser
from serv.settings import DEBUG

from api.models import Record, Doctor, Moderator, KeysToken, ChildRecord

class Octopus(APIView, metaclass=ABCMeta):
    cryp = Cryptographer()

    def get(self, req, token=""):
        token = get_object_or_404(KeysToken.objects.all(), token=token)
        if token.is_valid():
            user = token.user
            try:
                raw_data = self.work(req, user)
            except ObjectDoesNotExist:
                return Response(status=403)
            except NoUser:
                return Response(status=418)
            return Response(data=raw_data, status=200)
        return Response(status=401)

    @abstractmethod
    def work(self, req, user):
        if DEBUG:
            print(req, user)

class OctopusModerator(Octopus):
    def work(self, req, user):
        if DEBUG:
            print(req)
        try:
            mod = Moderator.objects.get(user=user)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

        doctors_query = Doctor.objects.filter(hospital=mod.hospital)
        doctors = [d.get_obj() for d in doctors_query]

        return {
            'doc': doctors,
            'hos': mod.hospital.get_obj(),
            'usr': user.get_obj()
        }

class OctopusRecord(Octopus):
    def work(self, req, user):
        if DEBUG:
            print(req)
        try:
            rec = Record.objects.get(owner=user)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist
        return {
            'rec': rec.get_obj(),
            'usr': user.get_obj()
        }

class OctopusDoctor(Octopus):
    def work(self, req, user):
        if DEBUG:
            print(req)
        try:
            doc = Doctor.objects.get(user=user)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist
        return doc.get_obj_hospital()

class OctopusRecordDoctor(Octopus):
    def work(self, req, user):
        params = req.query_params
        try:
            rec = Record.objects.get(serial_number=params['id'])
            rec_user = rec.owner
            data = {
                'rec': rec.get_obj(),
                'usr': rec_user.get_obj(),
            }
        except ObjectDoesNotExist:
            try:
                rec = ChildRecord.objects.get(serial_number=params['id'])
                data = rec.get_obj()
            except ObjectDoesNotExist:
                raise NoUser
        if not Doctor.objects.get(user=user):
            raise ObjectDoesNotExist
        return data


class OctopusRecordAmbulance(Octopus):
    def work(self, req, user):
        params = req.query_params
        try:
            rec = Record.objects.get(serial_number=params['id'])
            rec_user = rec.owner
            data = {
                'rec': rec.get_ambulace_obj(),
                'usr': rec_user.get_obj(),
            }
        except ObjectDoesNotExist:
            try:
                rec = ChildRecord.objects.get(serial_number=params['id'])
                data = rec.get_obj()
            except ObjectDoesNotExist:
                raise NoUser
        if not Doctor.objects.get(user=user):
            raise ObjectDoesNotExist
        return data

class OctopusChild(Octopus):
    def work(self, req, user):
        params = req.query_params
        try:
            child = ChildRecord.objects.get(serial_number=params['id'])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

        if child.parent == user:
            return child.get_obj()
        return None

class RecordOctopus(APIView):
    def get(self, req):
        try:
            raw_data = self._get_user_info_for_user(req)
        except NoUser:
            return Response(status=418)
        return Response(status=200, data=raw_data)
    def _get_user_info_for_user(self, req):
        params = req.query_params
        try:
            rec = Record.objects.get(serial_number=params['id'])
        except ObjectDoesNotExist:
            try:
                rec = ChildRecord.objects.get(serial_number=params['id'])
            except ObjectDoesNotExist:
                raise NoUser

        json_decoder = JSONDecoder()
        codes = [each['code'] for each in json_decoder.decode(rec.illnesses)]
        return {
            'codes': codes
        }
