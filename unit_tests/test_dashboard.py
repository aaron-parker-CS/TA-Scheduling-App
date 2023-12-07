from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class testLoadUsers(TestCase):
    def setUp(self):
        pass

    def test_load_users(self):
        pass

    def test_unsuccessful_load_users(self):
        pass

