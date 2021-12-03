import json
from django.test import TestCase, Client
from django.urls import reverse

from Crypto.Hash import SHA256

from serv.MRDApi import Cryptographer

from .models import User, ChildRecord, UnregisteredRecord, Record

class LoginTest(TestCase):
    fixtures = ['test_fixture1.json']

    def setUp(self):
        self.client = Client()

    def test_username_auth(self):
        data = json.dumps({'username' : 'test'},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:StartAuthSession')
        response = self.client.post(url, data=data, content_type="application/json")
        salt = response.json()['salt']
        token = response.json()['token']
        self.assertIn('salt', response.json())
        self.assertIn('token', response.json())
        my_hash = SHA256.new()
        my_hash.update(f'qwert{salt}'.encode())
        password = my_hash.hexdigest()
        data = json.dumps({'password' : password, 'token': token},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Authorization')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_phone_auth(self):
        data = json.dumps({'phone' : '9999999999'},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:StartAuthSession')
        response = self.client.post(url, data=data, content_type="application/json")
        salt = response.json()['salt']
        token = response.json()['token']
        self.assertIn('salt', response.json())
        self.assertIn('token', response.json())
        my_hash = SHA256.new()
        my_hash.update(f'qwert{salt}'.encode())
        password = my_hash.hexdigest()
        data = json.dumps({'password' : password, 'token': token},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Authorization')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_email_auth(self):
        data = json.dumps({'email' : 'test@dev.com'},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:StartAuthSession')
        response = self.client.post(url, data=data, content_type="application/json")
        salt = response.json()['salt']
        token = response.json()['token']
        self.assertEqual(response.status_code, 200)
        self.assertIn('salt', response.json())
        self.assertIn('token', response.json())
        my_hash = SHA256.new()
        my_hash.update(f'qwert{salt}'.encode())
        password = my_hash.hexdigest()
        data = json.dumps({'password' : password, 'token': token},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Authorization')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_wrong_creds_first(self):
        data = json.dumps({'username' : 'test'},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:StartAuthSession')
        response = self.client.post(url, data=data, content_type="application/json")
        salt = response.json()['salt']
        token = response.json()['token']
        self.assertEqual(response.status_code, 200)
        self.assertIn('salt', response.json())
        self.assertIn('token', response.json())
        my_hash = SHA256.new()
        my_hash.update(f'12345{salt}'.encode())
        password = my_hash.hexdigest()
        data = json.dumps({'password' : password, 'token': token},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Authorization')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_wrong_creds_second(self):
        data = json.dumps({'email' : 'dev'},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:StartAuthSession')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

class OctopusTest(TestCase):
    fixtures = ['test_fixture1.json']
    def setUp(self):
        self.client = Client()
        self.cryp = Cryptographer()

    def test_user_view(self):
        token = self.cryp.generate_token(User.objects.get(username='test')).token
        response = self.client.get(reverse('records:OctopusR', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('usr', response.json())
        self.assertIn('rec', response.json())

    def test_doctor_view(self):
        token = self.cryp.generate_token(User.objects.get(username='DOCTOR_MODERATOR_test')).token
        response = self.client.get(reverse('records:OctopusD', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.json())
        self.assertIn('hospital', response.json())
        self.assertIn('code', response.json())

    def test_moderator_view(self):
        token = self.cryp.generate_token(User.objects.get(username='DOCTOR_MODERATOR_test')).token
        response = self.client.get(reverse('records:OctopusM', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('usr', response.json())
        self.assertIn('doc', response.json())
        self.assertIn('hos', response.json())

    def test_forbidden_view(self):
        token = self.cryp.generate_token(User.objects.get(username='test')).token
        response = self.client.get(reverse('records:OctopusD', kwargs={'token': token}))
        self.assertEqual(response.status_code, 403)

    def test_bad_token_view(self):
        token = 'lul_it_is_some_token'
        response = self.client.get(reverse('records:OctopusR', kwargs={'token': token}))
        self.assertEqual(response.status_code, 404)

    def test_child_view(self):
        child = ChildRecord(
            serial_number='CHILD888',
            insurance_number='12345',
            illnesses='some kind of illnesses info',
            hospitals='some kind of hospitals info',
            recipes='some kind of recipies info',
            blood_type='some kind of bloodType info',
            first_name='some kind of firstName info',
            second_name='some kind of secondName info',
            last_name='some kind of lastName info',
            birthday='2020-4-1',
            parent=User.objects.get(username='test')
        )
        child.save()
        token = self.cryp.generate_token(User.objects.get(username='test')).token
        url = reverse('records:OctopusC', kwargs={'token': token}) + "?id=CHILD888"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('insurance_number', response.json())
        self.assertIn('illnesses', response.json())
        self.assertIn('hospitals', response.json())
        self.assertIn('recipes', response.json())
        self.assertIn('blood_type', response.json())
        self.assertIn('first_name', response.json())
        self.assertIn('second_name', response.json())
        self.assertIn('last_name', response.json())
        self.assertIn('birthday', response.json())

    def test_child_for_doctor_view(self):
        child = ChildRecord(
            serial_number='CHILD888',
            insurance_number='12345',
            illnesses='some kind of illnesses info',
            hospitals='some kind of hospitals info',
            recipes='some kind of recipies info',
            blood_type='some kind of bloodType info',
            first_name='some kind of firstName info',
            second_name='some kind of secondName info',
            last_name='some kind of lastName info',
            birthday='2020-4-1',
            parent=User.objects.get(username='test')
        )
        child.save()
        dmt = User.objects.get(username='DOCTOR_MODERATOR_test')
        token = self.cryp.generate_token(dmt).token
        url = reverse('records:OctopusRD', kwargs={'token': token}) + "?id=CHILD888"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('insurance_number', response.json())
        self.assertIn('illnesses', response.json())
        self.assertIn('hospitals', response.json())
        self.assertIn('recipes', response.json())
        self.assertIn('blood_type', response.json())
        self.assertIn('first_name', response.json())
        self.assertIn('second_name', response.json())
        self.assertIn('last_name', response.json())
        self.assertIn('birthday', response.json())

    def test_user_for_doctor_view(self):
        dmt = User.objects.get(username='DOCTOR_MODERATOR_test')
        token = self.cryp.generate_token(dmt).token
        url = reverse('records:OctopusRD', kwargs={'token': token}) + "?id=RY2FPt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('usr', response.json())
        self.assertIn('rec', response.json())

    def test_user_for_ambulance_view(self):
        token = self.cryp.generate_token(User.objects.get(username='DOCTOR_MODERATOR_test')).token
        url = reverse('records:OctopusRA', kwargs={'token': token}) + "?id=RY2FPt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('rec', response.json())
        self.assertIn('usr', response.json())

class RegisterTest(TestCase):
    fixtures = ['test_fixture1.json']
    def setUp(self):
        self.client = Client()
        self.cryp = Cryptographer()

    def test_registration(self):
        user_data = {
            'username': 'test2',
            'password': 'qwert',
            'first_name': 'kek1',
            'second_name': 'kek2',
            'last_name': 'kek3',
            'email': 'test2@dev.com',
            'telephone': '9797777777',
            'country_code': '7',
        }
        record_data = {
            'insurance_number': '1234678900987654',
            'blood_type': "0(I) Rh-",
            'illnesses': '[]',
            'contacts' : '[]',
            'recipes': '[]',
            'children': '[]'
        }
        salt_response = self.client.get(reverse('records:Registration'))

        self.assertEqual(salt_response.status_code, 200)
        self.assertIn('salt', salt_response.json())

        salt = salt_response.json()['salt']
        my_hash = SHA256.new()
        my_hash.update(f'qwert{salt}'.encode())
        user_data['password'] = f'{salt}${my_hash.hexdigest()}'

        data = json.dumps({'usr' : user_data, 'rec': record_data, 'id_exists': False},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Registration')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_registration_id_exists(self):
        new_unreg_rec = UnregisteredRecord(code="kek", serial_number="000001")
        new_unreg_rec.save()
        user_data = {
            'username': 'test3',
            'password': 'qwert',
            'first_name': 'kek1',
            'second_name': 'kek2',
            'last_name': 'kek3',
            'email': 'test3@dev.com',
            'telephone': '9797177777',
            'country_code': '7',
        }
        record_data = {
            'insurance_number': '1234678900987654',
            'blood_type': "0(I) Rh-",
            'illnesses': '[]',
            'contacts' : '[]',
            'recipes': '[]',
            'children': '[]'
        }
        mrd_data = {
            'id': '000001',
            'code': 'kek'
        }
        salt_response = self.client.get(reverse('records:Registration'))

        self.assertEqual(salt_response.status_code, 200)
        self.assertIn('salt', salt_response.json())

        salt = salt_response.json()['salt']
        my_hash = SHA256.new()
        my_hash.update(f'qwert{salt}'.encode())
        user_data['password'] = f'{salt}${my_hash.hexdigest()}'
        pre_dump_data = {
            'usr' : user_data,
            'rec': record_data,
            'mrd': mrd_data,
            'id_exists': True
        }
        data = json.dumps(pre_dump_data,
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Registration')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_wrong_creds_registration(self):
        user_data = {
            'username': 'test2',
            'password': 'qwert',
            'first_name': 'kek1',
            'second_name': 'kek2',
            'last_name': 'kek3',
            'email': 'test2@dev.com',
            'telephone': '9797777777',
            'country_code': '7',
        }
        record_data = {
            'insurance_number': '1234678900987654',
            'blood_type': "0(I) Rh-",
            'illnesses': '[]',
            'contacts' : '[]',
            'recipes': '[]',
            'children': '[]'
        }
        salt_response = self.client.get(reverse('records:Registration'))

        self.assertEqual(salt_response.status_code, 200)
        self.assertIn('salt', salt_response.json())

        salt = salt_response.json()['salt']
        my_hash = SHA256.new()
        my_hash.update(f'qwert{salt}'.encode())
        user_data['password'] = my_hash.hexdigest()

        data = json.dumps({'usr' : user_data, 'rec': record_data, 'id_exists': False},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Registration')
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

class EditTest(TestCase):
    fixtures = ['test_fixture1.json']
    def setUp(self):
        self.client = Client()
        self.cryp = Cryptographer()

    def test_editing(self):
        token = self.cryp.generate_token(User.objects.get(username='test')).token

        user_data = {
            "first_name": "firstNameTest1234",
            "last_name": "lastNameTest1234",
            "email": "1234@dev.com",
            "telephone": "8005553535",
            "second_name": "secondNameTest1234",
        }
        record_data = {
            'insurance_number' : 'test12345test',
            'blood_type': 'test'
        }
        data = json.dumps({'usr' : user_data, 'rec': record_data, 'token': token},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Editor')
        response = self.client.put(url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='test')
        record = Record.objects.get(owner=user)
        self.assertEqual(user_data['first_name'], user.first_name)
        self.assertEqual(user_data['second_name'], user.second_name)
        self.assertEqual(user_data['last_name'], user.last_name)
        self.assertEqual(user_data['email'], user.email)
        self.assertEqual(user_data['telephone'], user.telephone)
        self.assertEqual(record_data['blood_type'], record.blood_type)
        self.assertEqual(record_data['insurance_number'], record.insurance_number)

    def test_editing_wrong_creds(self):
        user = User.objects.get(username='test')
        token = self.cryp.generate_token(user).token

        user_data = {
            "username": "DOCTOR_MODERATOR_test",
            "first_name": "firstNameTest1234",
            "last_name": "lastNameTest1234",
            "email": "kek@dev.com",
            "telephone": "8005553535",
            "second_name": "secondNameTest1234",
        }
        record_data = {
            'insurance_number' : 'test12345test',
            'blood_type': 'test'
        }
        data = json.dumps({'usr' : user_data, 'rec': record_data, 'token': token},
                          separators=(',', ':'),
                          ensure_ascii=False
                          )
        url = reverse('records:Editor')
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue('usernameError' in response.json())
