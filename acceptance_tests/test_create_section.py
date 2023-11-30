from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course

class CreateSectionAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_section_url = reverse("createSection-view")
        self.course = Course(course_num=101, semester='Fa', year=2023, credits=3, description='Test Course')
        self.course.save()

    def test_successful_section_creation(self):
        response = self.client.post(self.create_section_url, {
            'section_num': 399,
            'type': "discussion",
            'course_num': self.course.__str__(),
            'start_time': "00:00",
            'end_time': "00:01",
            'tuesday': True,
            'location': "EMS",
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Section created successfully", response.content.decode('utf-8'))

    def test_section_number_validation_low(self):
        response = self.client.post(self.create_section_url, {
            'section_num': 100,
            'course_num': self.course.__str__(),
            'section_type': "Dis",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
        })

        self.assertNotEqual(response.status_code, 200)
        self.assertIn("Section number must be between 100 and 999", response.content.decode('utf-8'))

    def test_section_number_validation_high(self):
        response = self.client.post(self.create_section_url, {
            'section_num': 1000,
            'course_num': self.course.__str__(),
            'section_type': "lecture",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
        })

        self.assertNotEqual(response.status_code, 200)
        self.assertIn("Section number must be between 100 and 999", response.content.decode('utf-8'))

    def test_missing_required_fields_course_num(self):
        response = self.client.post(self.create_section_url, {
            'section_num': 402,
            'section_type': "discussion",
            'section_is_on_tuesday': True,
            'section_is_on_thursday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:11",
            # Missing'course_num''
        })

        self.assertNotEqual(response.status_code, 200)
        self.assertIn("This field is required", response.content.decode('utf-8'))

    # Repeat similar structure for other tests...

if __name__ == '__main__':
    import unittest
    unittest.main()