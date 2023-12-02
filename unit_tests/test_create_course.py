from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class CreateCourseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_course_success(self):
        """
        Test successful creation of a course through POST request
        """
        response = self.client.post('/createCourse/', {
            'course_num': 101,
            'semester': 'Fa',
            'year': 2023,
            'credits': 3,
            'description': "Intro to Testing"
        })
        self.assertEqual(response.status_code, 302, msg="Failed to create a course successfully.")
        self.assertTrue(Course.objects.filter(course_num=101).exists(), msg="Course does not exist in the database.")

    def test_course_number_validation(self):
        """
        Test course number validation (must be between 100 and 999) through POST request
        """
        response = self.client.post('/createCourse/', {
            'course_num': 99,  # Invalid course number
            'year': 2023,
            'credits': 3
        })
        self.assertNotEqual(response.status_code, 404, msg="Expected a different status code.")
        self.assertFalse(Course.objects.filter(course_num=99).exists(), msg="Course with invalid number exists.")

    def test_course_number_validation_high(self):
        """
        Test course number validation for a number too high.
        """
        response = self.client.post('/createCourse/', {
            'course_num': 1000,  # Invalid course number
            'year': 2023,
            'credits': 3,
            'description': "Test Course High Number"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to handle high course number properly.")
        self.assertFalse(Course.objects.filter(course_num=1000).exists(), msg="Course with high number exists.")

    def test_year_validation_low(self):
        """
        Test year validation for a year too low (before 2000).
        """
        response = self.client.post('/createCourse/', {
            'course_num': 106,
            'semester': 'Fa',
            'year': 1999,  # Invalid year
            'credits': 3,
            'description': "Test Course Early Year"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to handle low year properly.")
        self.assertFalse(Course.objects.filter(course_num=106).exists(), msg="Course with early year exists.")

    def test_year_validation_high(self):
        """
        Test year validation for a year too high (after 9999).
        """
        response = self.client.post('/createCourse/', {
            'course_num': 107,
            'semester': 'Fa',
            'year': 10000,  # Invalid year
            'credits': 3,
            'description': "Test Course Future Year"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to handle high year properly.")
        self.assertFalse(Course.objects.filter(course_num=107).exists(), msg="Course with future year exists.")

    def test_credits_default_value(self):
        """
        Test that the default value of credits is 1 if not specified.
        """
        response = self.client.post('/createCourse/', {
            'course_num': 108,
            'semester': 'Fa',
            'year': 2023,
            'description': "Test Course Default Credits"
        })
        print(response.content.decode())
        self.assertEqual(response.status_code, 302, msg="Failed to set default credits value.")
        self.assertTrue(Course.objects.filter(course_num=108, credits=1).exists(),
                        msg="Course with default credits does not exist.")

    def test_duplicate_course_number(self):
        """
        Test that creating a course with a duplicate course number through POST request is handled
        """
        self.client.post('/createCourse/', {'course_num': 104, 'year': 2023, 'credits': 3})
        response = self.client.post('/createCourse/', {'course_num': 104, 'year': 2024, 'credits': 4})
        self.assertNotEqual(response.status_code, 404,
                            msg="Expected a different status code for duplicate course number.")
