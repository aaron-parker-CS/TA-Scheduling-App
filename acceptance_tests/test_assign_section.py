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
        self.test_course = Course.objects.create(course_num=555, semester='Fa', year=2025, description='Intro to '
                                                                                                       'testing')
        self.test_course.save()
        self.test_section = Section.objects.create(course=self.test_course,
                                                   section_num=401,
                                                   section_is_on_monday=True,
                                                   section_start_time='09:30',
                                                   section_end_time='10:30',
                                                   location='Testing room')
        self.test_section.save()
        self.client.post('/', {'username': 'admin', 'password': 'adminpassword'})
        self.client.post('/assignCourse/', {'userId': self.admin_user.id, 'courseId': self.test_course.id})

    def test_assign_section(self):
        self.client.post('/assignSection/', {'userId': self.admin_user.id, 'sectionId': self.test_section.id})
        resp = self.client.get('/dashboard/', {})
        user_assignment = UserAssignment.objects.filter(user_id=self.admin_user, course=self.test_course,
                                                        section=self.test_section).first()
        self.assertContains(resp, user_assignment.str_section())

    def test_assign_section_twice(self):
        self.client.post('/assignSection/', {'userId': self.admin_user.id, 'sectionId': self.test_section.id})
        resp = self.client.post('/assignSection/', {'userId': self.admin_user.id, 'sectionId': self.test_section.id})
        self.assertContains(resp, 'Unable to assign user')

