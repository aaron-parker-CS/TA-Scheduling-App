from django.test import TestCase

from Classes.DashboardClass import DashboardClass
from TAScheduler.models import User, Course, Section, UserAssignment


class TestLoadUsers(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', first_name='John', last_name='Doe',
                                              email='john@example.com')
        self.user2 = User.objects.create_user(username='use', first_name='Jon', last_name='oe',
                                              email='johdfn@example.com')
        self.dashboard = DashboardClass()

    def test_load_users(self):
        li = []
        self.users = self.dashboard.loadUsers(li)
        self.assertGreater(len(li), 1)

    def test_load_users_empty(self):
        # Check for exactly 1; because the header
        User.objects.all().delete()

        li = []
        self.dashboard.loadUsers(li)

        self.assertEqual(len(li), 1)
        self.assertIn(['Username', 'First Name', 'Last Name', 'User Type', 'Email', 'Phone Number', 'Skills',
                       'Assigned Courses', 'Assigned Sections'], li)

    def test_user_details(self):
        li = []
        self.dashboard.loadUsers(li)
        self.assertEqual(li[1],
                         ['user1', 'John', 'Doe', 'Supervisor', 'john@example.com', 'N/A', '', '', ''])

    def test_load_courses_empty(self):
        li = []
        self.dashboard.loadCourses(li)
        self.assertEqual(len(li), 1, msg='Loading no courses should have been header row only.')

    def test_load_courses(self):
        li = []
        new_course = Course(course_num=351, semester='Fa', year=2023, description='Test Course')
        new_course.save()
        self.dashboard.loadCourses(li)
        self.assertEqual(len(li), 2, msg='Loading courses failed to load header row and course row.')

    def test_load_sections_empty(self):
        li = []
        self.dashboard.loadSections(li)
        self.assertEqual(len(li), 1,
                         msg='Loading no sections should have been of length 1 to include only header row.')

    def test_load_sections(self):
        li = []
        new_course = Course(course_num=351, semester='Fa', year=2023, description='Test Course')
        new_course.save()
        new_section = Section(course=new_course, section_num=400, section_start_time='00:01', section_end_time='00:02',
                              section_type='LEC', location='Test')
        new_section.save()
        self.dashboard.loadSections(li)
        self.assertEqual(len(li), 2,
                         msg='Loading sections should be of length 2 to include only header and new section')

    def test_load_TAUsers(self):
        li = []
        self.dashboard.loadTAUsers(li)
        self.assertEqual(len(li), 3)
        self.assertNotIn('Username', li[0], msg='Username should not be included in the list')

    def test_load_items(self):
        li = []
        self.dashboard.loadItems(UserAssignment, li)
        self.assertEqual(len(li), 0, msg='LoadItems should not populate list as no UserAssignments exist.')

    def test_load_items_sections(self):
        li = []
        new_course = Course(course_num=351, semester='Fa', year=2023, description='Test Course')
        new_course.save()
        new_section = Section(course=new_course, section_num=400, section_start_time='00:01', section_end_time='00:02',
                              section_type='LEC', location='Test')
        new_section.save()
        self.dashboard.loadItems(Section, li)
        self.assertEqual(len(li), 2,
                         msg='Load items by type should return the same value as that specific load item type')