from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class CreateCourseTest(TestCase):
    #TODO: Write create course unit tests. The ones here before were acceptance tests.
    def setUp(self):
        pass
