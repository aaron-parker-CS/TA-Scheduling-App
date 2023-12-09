from django.test import TestCase
from Classes.AuthClass import auth_type
from TAScheduler.models import User, Info


class TestAuthType(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'Th1$ 1$ @ t3$t')
        self.test_user.save()
        self.test_types = Info.objects.create(user=self.test_user)
        self.test_types.save()

    def test_auth_type(self):
        result = auth_type(self.test_user)
        self.assertEqual('Supervisor', result, msg='auth_type() fails to return correct user type')

    def test_auth_type_no_info(self):
        user2 = User.objects.create_user('test2', 'test2@example.com', 'This password is not great')
        user2.save()
        result = auth_type(user2)
        self.assertEqual('Supervisor', result, msg='auth_type() fails to generate user info model when no info exists.')
