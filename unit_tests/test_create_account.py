from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class TestCreateAccount(TestCase):
    test_user = None
    user_info = None
    test_client = None

    def setUp(self):
        self.test_client = Client()
        self.test_user = User(username="test", password="password", email='test.account@email.com')
        self.user_info = Info(user=self.test_user)
        self.test_user.info.type = self.test_user.info.TYPE_CHOICES[0]
        self.test_client.login(username=self.test_user.username, password=self.test_user.password)
        self.test_user.save()
        self.user_info.save()

    def test_create_account(self):
        resp = self.test_client.post('/createAccount/', {"username": "test.account", "password": "test",
                                                         'email': 'test', 'phone': 'test', 'address': 'test',
                                                         'type': 'TA'})
        self.assertEqual(resp.context["message"], 'Creation successful',
                         msg='Message not shown on account creation')
        self.assertNotEqual(None, User.objects.get(username='test.account'), msg="User account not successfully "
                                                                                 "created.")

    def test_no_admin_redirect(self):
        self.test_user.info.type = self.test_user.info.TYPE_CHOICES[2]
        resp = self.test_client.get('/createAccount/')
        self.assertEqual(resp.status_code, 403, msg="Forbidden message not given to non-admin user.")

    def test_user_created_with_info(self):
        resp = self.test_client.post('/createAccount/', {"username": "test.account", "password": "test",
                                                         'email': 'test', 'phone': 'test', 'address': 'test',
                                                         'type': 'TA'})
        new_id = User.objects.get(username='test.account')
        self.assertNotEqual(None, Info.objects.get(user=new_id),
                            msg="User was created without an info model assigned to it.")

    def test_user_already_exists(self):
        resp = self.test_client.post('/createAccount/', {"username": self.test_user.username, "password": "test",
                                                         'email': 'test', 'phone': 'test', 'address': 'test',
                                                         'type': 'TA'})
        self.assertEqual(resp.context['message'], 'User already exists',
                         msg='Duplicate user creation does not show the proper error message')

    def test_null_values(self):
        resp = self.test_client.post('/createAccount/', {"username": '', "password": '', 'email': 'test',
                                                         'phone': 'test', 'type': 'TA'})
        self.assertEqual(resp.context['message'], 'Enter required fields.',
                         msg='Null required values do not show the required error message.')
