from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Hospital
from .models import DeliveryMap
from serv.settings import DEBUG


class PartnersMapViewer(APIView):
    def get(self, req):
        if DEBUG:
            print(req)
        hospitals = Hospital.objects.all()
        data = []
        for each in hospitals:
            data.append(each.get_map_obj())
        # print(data)
        return Response(data=data, status=200)


class SelfDeliveryMapMarkers(APIView):
    def get(self, req):
        if DEBUG:
            print(req)
        points = DeliveryMap.objects.all()
        data = []
        for each in points:
            data.append(each.get_map_obj())
        return Response(data=data, status=200)
