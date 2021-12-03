from django.db.models import ObjectDoesNotExist

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from serv.MRDApi import Cryptographer

from api.models import User, KeysToken

class StartAuthSession(APIView):
    cryp = Cryptographer()

    def post(self, req):
        if req.data.get('username'):
            try:
                user = User.objects.get(username=req.data.get('username'))
            except ObjectDoesNotExist:
                return Response(status=404)
        elif req.data.get('phone'):
            try:
                user = User.objects.get(telephone=req.data.get('phone'))
            except ObjectDoesNotExist:
                return Response(status=404)
        elif req.data.get('email'):
            try:
                user = User.objects.get(email=req.data.get('email'))
            except ObjectDoesNotExist:
                return Response(status=404)
        else:
            return Response(status=404)

        salt = user.get_salt()
        token = self.cryp.generate_token(user)
        raw_data = {'salt': salt, 'token': token.token}
        return Response(data=raw_data, status=200)

    def _displaymatch(self, match):
        print('\n\n', match, '\n\n')
        if match is None:
            return None
        return '<Match: %r, groups=%r>' % (match.group(), match.groups())


class Authorization(APIView):
    cryp = Cryptographer()

    def post(self, req):
        token_data = req.data.get('token') or req.query_params['token']
        token = get_object_or_404(
            KeysToken.objects.all(),
            token=token_data)
        if token.is_valid():
            user = token.user
            password = req.data.get('password') or req.query_params['password']
            if user.login(password):
                token.update_activity()
                token.login()
                return Response(status=200)
            else:
                token.delete()
                return Response(status=404)
        else:
            return Response(status=401)
