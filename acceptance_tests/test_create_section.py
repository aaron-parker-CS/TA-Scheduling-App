from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course, User

class CreateSectionAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_section_url = reverse("createSection-view")
        self.admin_user = User.objects.create_user('admin', 'admin@example.com')
        self.admin_user.set_password('adminpassword')
        self.admin_user.save()
        self.client.post('/', {'username': 'admin', 'password': 'adminpassword'})
        self.course = Course(course_num=101, semester='Fa', year=2023, description='Test Course')
        self.course.save()

    def test_successful_section_creation(self):
        response = self.client.post(self.create_section_url, {
            'section': 399,
            'type': "Dis",
            'course_num': self.course.__str__(),
            'start_time': "00:00",
            'end_time': "00:01",
            'tuesday': True,
            'location': "EMS",
        })
        self.assertRedirects(response, '/dashboard/')

    def test_section_number_validation_low(self):
        response = self.client.post(self.create_section_url, {
            'section_num': 800,
            'course_num': self.course.__str__(),
            'type': "Dis",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:12",
        })
        self.assertEqual(response.status_code, 200, "Status code misalignment. Problems may have occured.")
        self.assertContains(response, "Validation Error")

    def test_section_number_validation_high(self):
        response = self.client.post(self.create_section_url, {
            'section_num': 1000,
            'course_num': self.course.__str__(),
            'section_type': "lecture",
            'section_is_on_monday': True,
            'section_is_on_wednesday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:12",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Validation Error")

    def test_missing_required_fields_course_num(self):
        response = self.client.post(self.create_section_url, {
            'section': 402,
            'section_type': "discussion",
            'section_is_on_tuesday': True,
            'section_is_on_thursday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:12",
            # Missing 'course_num''
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Validation Error")

    def test_duplicate_section_case(self):
        self.client.post(self.create_section_url, {
            'section': 402,
            'course_num': self.course.__str__(),
            'type': "Dis",
            'section_is_on_tuesday': True,
            'section_is_on_thursday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:12",
        })
        response = self.client.post(self.create_section_url, {
            'section': 402,
            'course_num': self.course.__str__(),
            'type': "Dis",
            'section_is_on_tuesday': True,
            'section_is_on_thursday': True,
            "location": "EMS",
            "start_time": "11:11",
            "end_time": "11:12",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Duplicate Section Number")


