import random
import string
from rest_framework import serializers as ser
from api.models import Record, ICD, User, Hospital, ChildRecord, NewPartnerModel


class RecordSerializer(ser.Serializer):
    serial_number = ser.CharField()
    insurance_number = ser.CharField(required=False)
    contacts = ser.JSONField(required=False)
    hospitals = ser.JSONField(required=False)
    recipes = ser.JSONField(required=False)
    blood_type = ser.CharField(required=False)
    children = ser.JSONField(required=False)
    illnesses = ser.JSONField(required=False)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.insurance_number = validated_data.get(
            'insurance_number', instance.insurance_number)
        instance.illnesses = validated_data.get(
            'illnesses', instance.illnesses)
        instance.contacts = validated_data.get('contacts', instance.contacts)
        instance.hospitals = validated_data.get(
            'hospitals', instance.hospitals)
        instance.recipes = validated_data.get('recipes', instance.recipes)
        instance.blood_type = validated_data.get(
            'blood_type', instance.blood_type)
        instance.children = validated_data.get('children', instance.children)
        instance.save()
        return instance


class UserSerializer(ser.Serializer):
    username = ser.CharField()
    password = ser.CharField()
    email = ser.CharField()
    first_name = ser.CharField()
    last_name = ser.CharField()
    second_name = ser.CharField()
    telephone = ser.CharField()
    country_code = ser.CharField()

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.second_name = validated_data.get(
            'second_name', instance.second_name)
        instance.telephone = validated_data.get(
            'telephone', instance.telephone)
        instance.country_code = validated_data.get(
            'country_code', instance.country_code)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class ICDSerializer(ser.Serializer):
    code = ser.CharField()
    info = ser.CharField()

    def create(self, validated_data):
        return ICD.objects.create(**validated_data)


class HospitalSerializer(ser.Serializer):
    region = ser.CharField()
    country = ser.CharField()
    city = ser.CharField()
    street = ser.CharField()
    geo_data = ser.CharField()
    post_index = ser.CharField()
    name = ser.CharField()
    additional = ser.CharField()
    code = ser.CharField(required=False)

    def create(self, validated_data):
        code = ''.join(
            [random.choice(string.digits + string.ascii_uppercase) for i in range(10)])
        validated_data['code'] = code
        return Hospital.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.region = validated_data.get('region', instance.region)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.geo_data = validated_data.get('geo_data', instance.geo_data)
        instance.post_index = validated_data.get(
            'post_index', instance.post_index)
        instance.name = validated_data.get('name', instance.name)
        instance.additional = validated_data.get(
            'additional', instance.additional)
        instance.save()
        return instance


class ChildRecordSerializer(ser.Serializer):
    serial_number = ser.CharField()
    insurance_number = ser.CharField()
    illnesses = ser.CharField()
    recipes = ser.CharField()
    blood_type = ser.CharField()
    first_name = ser.CharField()
    second_name = ser.CharField()
    last_name = ser.CharField()
    birthday = ser.DateField()

    def create(self, validated_data):
        return ChildRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.serial_number = validated_data.get(
            'serial_number', instance.serial_number)
        instance.insurance_number = validated_data.get(
            'insurance_number', instance.insurance_number)
        instance.illnesses = validated_data.get(
            'illnesses', instance.illnesses)
        instance.recipes = validated_data.get('recipes', instance.recipes)
        instance.blood_type = validated_data.get(
            'blood_type', instance.blood_type)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.second_name = validated_data.get(
            'second_name', instance.second_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.save()
        return instance


class NewPartnerSerializer(ser.Serializer):
    address = ser.CharField()
    company = ser.CharField()
    phone = ser.CharField()
    name = ser.CharField()
    email = ser.CharField()

    def create(self, validated_data):
        return NewPartnerModel.objects.create(**validated_data)
