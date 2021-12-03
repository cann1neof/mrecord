from django.contrib import admin

from api.models import Record, UnregisteredRecord, User, Hospital, Moderator, Doctor, KeysToken, Event

admin.site.register(Record)
admin.site.register(UnregisteredRecord)
admin.site.register(User)
admin.site.register(Hospital)
admin.site.register(Moderator)
admin.site.register(Doctor)
admin.site.register(KeysToken)
admin.site.register(Event)
