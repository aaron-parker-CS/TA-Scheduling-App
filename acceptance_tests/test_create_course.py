from django.test import TestCase, Client
from TAScheduler.models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from TAScheduler.models import User, Info


class CreateCourseTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Creating a user with privileges to create courses
        self.admin_user = User.objects.create_user('admin', 'admin@example.com', 'adminpassword')
        self.client.login(username='admin', password='adminpassword')


def test_successful_course_creation(self):
    response = self.client.post('/create-course/', {
        'course_num': 361,
        'semester': 'Fall',
        'year': 2023,
        'credits': 3,
        'description': 'Introduction to Testing'
    })
    self.assertRedirects(response, '/dashboard/')


def test_course_creation_validation_errors(self):
    response = self.client.post('/create-course/', {
        # Deliberately leaving out 'course_num' and 'year' to trigger validation errors
        'semester': 'Fall',
        'credits': 3,
        'description': 'Test Course'
    })
    self.assertEqual(response.status_code, 200)
    self.assertIn("Validation Error:", response.content.decode())


def test_duplicate_course_number_error(self):
    # Create a course first
    Course.objects.create(course_num=362, semester='Fall', year=2023, credits=3, description='Initial Course')
    # Attempt to create another course with the same course number
    response = self.client.post('/create-course/', {
        'course_num': 362,
        'semester': 'Fall',
        'year': 2023,
        'credits': 3,
        'description': 'Duplicate Course'
    })
    self.assertEqual(response.status_code, 200)
    self.assertIn("Duplicate course number. Please use a unique number.", response.content.decode())


def test_course_creation_with_invalid_data(self):
    response = self.client.post('/create-course/', {
        'course_num': 363,
        'semester': 'InvalidSemester',  # Invalid semester
        'year': 1999,  # Invalid year
        'credits': 3,
        'description': 'Test Course'
    })
    self.assertEqual(response.status_code, 200)
    self.assertIn("Validation Error:", response.content.decode())
