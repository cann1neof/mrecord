'''
Взято с Хабра. Спасибо автору большое =)
https://habr.com/ru/post/452042/
'''
from datetime import datetime

from Crypto.Hash import SHA256

from api.models import KeysToken

class NotValid(Exception):
    def __str__(self):
        return 'kek, not valid'

class NoUser(Exception):
    def __str__(self):
        return 'kek, no user'

class Cryptographer():
    def timestamp(self):
        now = datetime.now()
        seconds = int((now - datetime(2001, 1, 1)).total_seconds())
        return seconds

    def generate_token(self, user):
        timestamp = str(self.timestamp())
        my_hash = SHA256.new()
        my_hash.update(timestamp.encode())
        my_hash = my_hash.hexdigest()
        return self._save_token(my_hash, user)

    def _save_token(self, token, user):
        token = KeysToken(
            user=user,
            token=token
        )
        token.save()
        return token
