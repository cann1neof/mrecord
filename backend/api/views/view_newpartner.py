import random

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import NewPartnerModel, KeysToken

from api.serializer import NewPartnerSerializer


class NewPartner(APIView):
    def post(self, req):
        new_partner = req.data.get('new_partner')
        new_partner_ser = NewPartnerSerializer(data=new_partner)
        if new_partner_ser.is_valid():
            new_partner_ser.save()
            return Response(status=201)
        return Response(status=400)

    def get(self, req):
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=req.GET['token'])
        user = token.user
        if token.is_valid() and user.is_staff:
            new_partner = self._get_random_partner()
            return Response(status=200, data=new_partner)
        return Response(status=403)

    def _get_random_partner(self):
        try:
            partners = NewPartnerModel.objects.filter(available=True)
            cur_partner = random.choice(partners)
            cur_partner.available = False
            cur_partner.save()
        except IndexError:
            return 'nothing new('
        return cur_partner.get_obj()
