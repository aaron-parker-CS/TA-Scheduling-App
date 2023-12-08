from django.test import TestCase
from Classes.LoginClass import LoginClass
from TAScheduler.models import User, Info


class TestLogin(TestCase):
    test_user = None
    test_types = None
    login_validator = None

    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'Th1$ 1$ @ t3$t')
        self.test_user.save()
        self.test_types = Info.objects.create(user=self.test_user)
        self.test_types.save()
        self.login_validator = LoginClass()

    def test_validate_fields(self):
        result = self.login_validator.validate_login_fields({},'test', 'Th1$ 1$ @ t3$t')
        self.assertEqual('Success', result, msg='Valid login fields fails to return the correct result')

    def test_validate_fields_missing_username(self):
        result = self.login_validator.validate_login_fields({},'', 'Th1$ 1$ @ t3$t')
        self.assertEqual('This field is required', result,
                         msg='Validate login does not return the correct message for missing username field')

    def test_validate_fields_missing_password(self):
        result = self.login_validator.validate_login_fields({},'test', '')
        self.assertEqual('This field is required', result,
                         msg='Validate login does not return the correct message for missing password field')

    def test_validate_fields_invalid_username(self):
        result = self.login_validator.validate_login_fields({},'This does not exist', 'Th1$ 1$ @ t3$t')
        self.assertEqual('Incorrect username', result,
                         msg='Validate login does not return the correct message for invalid username')

    def test_validate_fields_invalid_username(self):
        result = self.login_validator.validate_login_fields({},'test', 'Bad password')
        self.assertEqual('Incorrect password', result,
                         msg='Validate login does not return the correct message for invalid password')


    def test_auth_type(self):
        result = self.login_validator.auth_type(self.test_user)
        self.assertEqual('SU', result, msg='auth_type() fails to return correct user type')

    def test_auth_type_no_info(self):
        user2 = User.objects.create_user('test2', 'test2@example.com', 'This password is not great')
        user2.save()
        result = self.login_validator.auth_type(user2)
        self.assertEqual('SU', result, msg='auth_type() fails to generate user info model when no info exists.')
