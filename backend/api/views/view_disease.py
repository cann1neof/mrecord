from django.db.models import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ICD
from serv.settings import DEBUG


class Disease(APIView):
    def get(self, req, disease):
        if DEBUG:
            print(req)
        try:
            rec = ICD.objects.get(code=disease)
        except ObjectDoesNotExist:
            return Response(status=404)
        return Response(status=200, data={'code': rec.code, 'info': rec.info})
