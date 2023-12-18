from django.test import TestCase, Client
from TAScheduler.models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from TAScheduler.models import User, Info


class CreateCourseTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Creating a user with privileges to assign courses
        self.admin_user = User.objects.create_user('admin', 'admin@example.com')
        self.admin_user.set_password('adminpassword')
        self.admin_user.save()
        self.client.post('/', {'username': 'admin', 'password': 'adminpassword'})
        self.test_course = Course.objects.create(course_num=555, semester='Fa', year=2025, description='Intro to '
                                                                                                       'testing')
        self.test_course.save()

    def test_assign_success(self):
        self.client.post('/assignCourse/', {'userId': self.admin_user.id, 'courseId': self.test_course.id})
        resp = self.client.get('/dashboard/', {})
        self.assertContains(resp, self.test_course.__str__())

    def test_assign_twice(self):
        self.client.post('/assignCourse/', {'userId': self.admin_user.id, 'courseId': self.test_course.id})
        self.client.get('/dashboard/', {})
        resp = self.client.post('/assignCourse/', {'userId': self.admin_user.id, 'courseId': self.test_course.id})
        self.assertContains(resp, 'Unable to assign user')
