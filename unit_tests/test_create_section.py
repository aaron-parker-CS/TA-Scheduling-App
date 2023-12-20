import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError
from Classes.SectionClass import SectionClass

class CreateSectionTest(TestCase):
    def setUp(self):
        self.create_section_url = reverse("createSection-view")
        # create course
        self.course = Course(course_num=101, semester='Fa', year=2023,
                             description='Test Course')
        self.sectionHelper = SectionClass()
        self.course.save()
        self.now = datetime.datetime.now()
        self.later = self.now + datetime.timedelta(minutes=10)

    def test_populate_course_list(self):
        self.course_list = []
        self.course_list = self.sectionHelper.populate_course_list(self.course_list)
        self.assertTrue(len(self.course_list) > 0)

    def test_find_course_obj(self):
        course_id = "Fa2023: 101"
        courseObj = self.sectionHelper.find_course_obj(course_id)
        self.assertEqual(courseObj, self.course)

    def test_validate_time_success(self):
        result = self.sectionHelper.validate_time(self.now, self.later)
        self.assertTrue(result, msg='Validate time fails to return true for valid time comparison')

    def test_validate_time_fail(self):
        result = self.sectionHelper.validate_time(self.later, self.now)
        self.assertFalse(result, msg='Validate time fails to return false for first argument being chronologically '
                                     'after the second.')

    def test_validate_time_invalid_arg(self):
        with self.assertRaises(ValueError, msg='validate_time() fails to raise ValueError for invalid arguments.'):
            self.sectionHelper.validate_time([], 'string')

