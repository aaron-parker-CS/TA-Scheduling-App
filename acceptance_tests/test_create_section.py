from django.test import TestCase, Client
from TAScheduler.models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from TAScheduler.models import User, Info


class CreateSectionTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Creating a user with privileges to create courses
        self.course = Course(course_num=101, semester='Fa', year=2023, credits=3,
                             description='Test Course')
        # Ensure the course object is saved
        self.course.save()
        self.assertTrue(Course.objects.filter(course_num=101).exists(), 'Course creation unsuccessful')

        self.admin_user = User.objects.create_user('admin', 'admin@example.com', 'adminpassword')
        self.client.login(username='admin', password='adminpassword')

    def test_successful_section_creation(self):
        response = self.client.post("/createSection/", {
            'section': 401,
            'type': "discussion",
            'course_num': self.course.__str__(),
            'start_time': "00:00",
            'end_time': "00:01",
            'tuesday': True,
            'location': "EMS",
        })
        print("Response content:", response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, "Wrong status code for successful section creation")