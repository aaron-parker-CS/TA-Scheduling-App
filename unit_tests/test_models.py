from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class TestModels(TestCase):
    test_user = None
    test_section = None
    test_course = None
    test_assignment = None

    def setUp(self):
        self.test_user = User(username="test", password="pass", email="test.user@email.com")
        self.test_course = Course(course_num=351, semester="Fa", year=2023,
                                  description="Data Structures and Algorithms")
        self.test_section = Section(course_num=self.test_course, section_num=401, section_type="Lec",
                                    section_is_on_monday=True, section_is_on_wednesday=True, section_start_time="09:30",
                                    section_end_time="10:30", location="EMS180")
        self.test_assignment = UserAssignment(user_id=self.test_user, section_num=self.test_section)

    def test_delete_user(self):
        User.objects.filter(id=self.test_user.id).delete()
        self.assertEqual(None, self.test_assignment.id,
                         msg="Test assignment fails to delete upon user deletion, no cascades")

    def test_delete_course(self):
        Course.objects.filter(course_num=self.test_course.course_num).delete()
        self.assertEqual(None, self.test_section.id,
                         "Section fails to cascade the delete upon course deletion.")
        self.assertEqual(None, self.test_assignment.id,
                         "Assignment fails to cascade delete upon course deletion.")

    def test_delete_section(self):
        Section.objects.filter(id=self.test_section.id).delete()
        self.assertEqual(None, self.test_assignment.id,
                         "Assignment fails to cascade delete upon section deletion.")
        self.assertNotEqual(None, self.test_course.course_num, "Course deletes upon selection deletion.")
