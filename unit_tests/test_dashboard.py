from django.test import TestCase
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError
from Classes.DashboardClass import DashboardClass


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
        self.assertIn(['Username', 'First Name', 'Last Name', 'User Type', 'Email', 'Phone Number', 'Assigned Sections',
                       'Skills'], li)

    def test_user_details(self):
        li = []
        self.dashboard.loadUsers(li)
        self.assertEqual(li[1],
                         ['user1', 'John', 'Doe', 'SU', 'john@example.com', 'N/A', []])

