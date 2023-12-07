from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class CreateSectionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_section_url = reverse("createSection-view")
        # create course
        self.course = Course(course_num=101, semester='Fa', year=2023, credits=3,
                             description='Test Course')
        self.course.save()
        print(Course.objects.all())
        print(self.course.id)

    def test_create_section_success(self):
        # check for successful redirect with good form request.
        response = self.client.post("/createSection/", {
            'section': 399,
            'type': "Dis",
            'course_num': self.course.__str__(),
            'start_time': "00:00",
            'end_time': "00:01",
            'tuesday': True,
            'location': "EMS",
        })
        self.assertEqual(response.status_code, 200, msg="Failed to create a section successfully.")

    def test_section_number_validation_low(self):
        # Test section number validation (must be between 100 and 999) through POST request
        response = self.client.post(self.create_section_url, {
            'section': 100,
            'course_num': self.course.__str__(),
            'type': "Dis",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
        })
        self.assertNotEqual(response.status_code, 302, msg="Expected a different status code.")

    def test_section_number_validation_high(self):
        # Test section number validation for a number too high.
        response = self.client.post(self.create_section_url, {
            'section': 1000,
            'course_num': self.course.__str__(),
            'type': "Dis",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
        })
        self.assertNotEqual(response.status_code, 302, msg="Expected a different status code.")

    def test_missing_required_fields_course_num(self):
        # Create a section with missing course field.
        response = self.client.post(self.create_section_url, {
            'section': 402,
            'type': "Dis",
            'section_is_on_tuesday': True,
            'section_is_on_thursday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
            # Missing 'section_num''
        })
        self.assertNotEqual(response.status_code, 302, msg="Failed to handle missing field - course_num")

    def test_missing_required_fields_section_num(self):
        # Create a section with missing section field.
        response = self.client.post(self.create_section_url, {
            'course_num': self.course.__str__(),
            'type': "Dis",
            'section_is_on_tuesday': True,
            'section_is_on_thursday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
            # Missing 'section_num''
        })
        self.assertNotEqual(response.status_code, 302, msg="Failed to handle missing field - section_num")

    def test_duplicate_course_number(self):
        """ Test that creating a section with a duplicate course number through POST request is handled """
        # Create a section with duplicate course, number 101
        self.client.post(self.create_section_url, {
            'course_num': self.course.__str__(),
            'section': 101,
            'type': "Dis",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
        })

        # Attempt to create another section with the same course number.
        response = self.client.post(self.create_section_url, {
            'course_num': self.course.__str__(),
            'section': 101,
            'type': "Dis",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
        })
        print(response.content.decode())
        self.assertContains(response, "Duplicate Course Number")