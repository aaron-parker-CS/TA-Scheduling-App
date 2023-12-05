from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


class TestDashboard(TestCase):
    test_user = None
    test_client = None

    def setUp(self):
        self.test_client = Client()
        self.test_user = User(username="test", password="password")

    def test_no_login(self):
        # No login should redirect to the login screen
        resp = self.test_client.get("/dashboard/")
        self.assertRedirects(response=resp, expected_url='/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
