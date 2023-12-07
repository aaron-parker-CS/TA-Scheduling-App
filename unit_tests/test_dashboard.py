from django.test import TestCase
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError
from Classes.DashboardClass import DashboardClass


class TestLoadUsers(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', first_name='John', last_name='Doe',
                                              email='john@example.com')
        self.dashboard = DashboardClass()
    def test_load_users(self):
        li = []
        self.users = self.dashboard.loadUsers(li)
        self.assertGreater(len(li), 1)
