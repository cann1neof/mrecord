from datetime import datetime, timedelta
import json
import pytz
from django.db import models
from django.contrib.auth.models import User as default_user


class User(default_user):
    second_name = models.CharField(max_length=32, blank=True)
    is_moderator = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    telephone = models.CharField(max_length=32, blank=True, unique=False)
    country_code = models.IntegerField(blank=True)

    def login(self, password):
        if self.password.split('$')[1] == password:
            self.last_login = datetime.now()
            self.save()
            return True
        return False

    def get_obj(self):
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'second_name': self.second_name,
            'telephone': f'+{self.country_code}{self.telephone}',
            'username': self.username
        }

    def get_ambulace_obj(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'second_name': self.second_name,
        }

    def get_salt(self):
        return self.password.split('$')[0]

    def get_json(self):
        return json.dumps(
            self.get_obj(), separators=(
                ',', ':'), ensure_ascii=False)


class Hospital(models.Model):
    code = models.CharField(max_length=10, blank=True)
    region = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    geo_data = models.CharField(max_length=32)
    post_index = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    additional = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_obj(self):
        return {
            'address': {
                'region': self.region,
                'country': self.country,
                'city': self.city,
                'street': self.street,
                'geo_data': self.geo_data,
                'post_index': self.post_index,
            },
            'name': self.name,
            'additional': self.additional,
            'code': self.code,
        }

    def get_map_obj(self):
        return {
            'coords': [float(i) for i in self.geo_data.split(', ')],
            'text': self.additional,
            'headline': self.name
        }

    def get_json(self):
        return json.dumps(
            self.get_obj(), separators=(
                ',', ':'), ensure_ascii=False)


class Moderator(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(to=Hospital, on_delete=models.CASCADE)


class Doctor(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(to=Hospital, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, blank=True)

    def get_obj(self):
        return {
            'user': self.user.get_obj(),
            'code': self.code
        }

    def get_obj_hospital(self):
        return {
            'user': self.user.get_obj(),
            'hospital': self.hospital.get_obj(),
            'code': self.code
        }

    def __str__(self):
        return '{} {} {}, {}'.format(self.user.last_name,
                                     self.user.first_name,
                                     self.user.second_name,
                                     self.code)


class Record(models.Model):
    serial_number = models.CharField(max_length=6)
    insurance_number = models.CharField(max_length=16, blank=True, null=True)
    illnesses = models.TextField(blank=True)
    contacts = models.TextField(blank=True)
    hospitals = models.TextField(blank=True)
    recipes = models.TextField(blank=True)
    blood_type = models.TextField(blank=True)
    children = models.TextField(blank=True)
    owner = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    def __str__(self):
        return 'MRecord Token #{}'.format(self.serial_number)

    def get_obj(self):
        return {
            'serial_number': self.serial_number,
            'insurance_number': self.insurance_number,
            'illnesses': self.illnesses,
            'contacts': self.contacts,
            'hospitals': self.hospitals,
            'recipes': self.recipes,
            'blood_type': self.blood_type,
            'children': self.children,
        }

    def get_json(self):
        return json.dumps(
            self.get_obj(), separators=(
                ',', ':'), ensure_ascii=False)

    def get_ambulace_obj(self):
        return {
            'blood_type': self.blood_type,
            'insurance_number': self.insurance_number,
            'illnesses': self.illnesses,
            'recipes': self.recipes,
        }


class ICD(models.Model):
    code = models.TextField(max_length=4)
    info = models.TextField()


class UnregisteredRecord(models.Model):
    serial_number = models.CharField(max_length=6)
    code = models.CharField(max_length=8)


class KeysToken(models.Model):
    token = models.CharField(max_length=256)
    logginned = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(blank=True, null=True, default=None)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)

    def is_valid(self):
        utc = pytz.UTC
        now = utc.localize(dt=datetime.now())
        if self.last_activity is None or self.last_activity == '':
            ok_time = self.created_at + timedelta(minutes=5)
            if (ok_time - now) <= timedelta(minutes=5):
                return True
            else:
                self.delete()
                return False
        else:
            ok_time = self.last_activity + timedelta(minutes=10)
            if (ok_time-now) <= timedelta(minutes=10) and self.logginned:
                return True
            else:
                self.delete()
                return False

    def login(self):
        self.logginned = True
        self.save()

    def update_activity(self):
        utc = pytz.UTC
        now = utc.localize(dt=datetime.now())
        self.last_activity = now
        self.save()


class Event(models.Model):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    result = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class ChildRecord(models.Model):
    parent = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    serial_number = models.CharField(max_length=8)
    insurance_number = models.CharField(max_length=16, blank=True, null=True)
    illnesses = models.TextField(blank=True)
    hospitals = models.TextField(blank=True)
    recipes = models.TextField(blank=True)
    blood_type = models.TextField(blank=True)
    first_name = models.TextField()
    second_name = models.TextField()
    last_name = models.TextField()
    birthday = models.DateField()

    def get_obj(self):
        return{
            'insurance_number': self.insurance_number,
            'illnesses': self.illnesses,
            'hospitals': self.hospitals,
            'recipes': self.recipes,
            'blood_type': self.blood_type,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'last_name': self.last_name,
            'birthday': self.birthday,
        }


class MigrationToken(models.Model):
    token = models.TextField()
    user = models.ForeignKey(to=ChildRecord, on_delete=models.CASCADE)
    parent = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        utc = pytz.UTC
        now = utc.localize(dt=datetime.now())
        ok_time = self.created_at + timedelta(minutes=5)
        if now < ok_time:
            return True
        else:
            self.delete()
            return False


class NewPartnerModel(models.Model):
    address = models.TextField()
    company = models.TextField()
    phone = models.TextField()
    name = models.TextField()
    email = models.TextField()
    available = models.BooleanField(default=True)

    def get_obj(self):
        return {
            'address': self.address,
            'company': self.company,
            'phone': self.phone,
            'name': self.name,
            'email': self.email
        }
