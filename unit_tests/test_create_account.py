from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from Classes.CreateAccountClass import CreateAccountClass
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class TestCreateUser(TestCase):

    def test_proper_input(self):
        cac = CreateAccountClass()

        self.assertTrue(cac.create_user("username", "email", "password", "phone", "address", "type"))

    def test_empty_fields(self):
        cac = CreateAccountClass()

        with self.assertRaises(ValueError, msg='Class fails to produce correct value error on null argument'):
            cac.create_user("", "", "", "", "", "")

    def test_empty_username(self):
        cac = CreateAccountClass()

        with self.assertRaises(ValueError, msg='Class fails to produce correct value error on null argument'):
            cac.create_user("", "test", "test", "test", "test", "test")

    def test_empty_email(self):
        cac = CreateAccountClass()

        with self.assertRaises(ValueError, msg='Class fails to produce correct value error on null argument'):
            cac.create_user("test", "", "test", "test", "test", "test")

    def test_empty_password(self):
        cac = CreateAccountClass()

        with self.assertRaises(ValueError, msg='Class fails to produce correct value error on null argument'):
            cac.create_user("test", "test", "", "test", "test", "test")

    def test_empty_phone(self):
        cac = CreateAccountClass()

        with self.assertRaises(ValueError, msg='Class fails to produce correct value error on null argument'):
            cac.create_user("test", "test", "test", "", "test", "test")

    def test_empty_address(self):
        cac = CreateAccountClass()

        with self.assertRaises(ValueError, msg='Class fails to produce correct value error on null argument'):
            cac.create_user("test", "test", "test", "test", "", "test")

    def test_empty_type(self):
        cac = CreateAccountClass()

        with self.assertRaises(ValueError, msg='Class fails to produce correct value error on null argument'):
            cac.create_user("test", "test", "test", "test", "test", "")
