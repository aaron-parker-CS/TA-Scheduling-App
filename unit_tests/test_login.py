from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError

class TestLogin(TestCase):
    test_user = None
    test_client = None

    def setUp(self):
        self.test_client = Client()
        self.test_user = User(username="test", password="password", email="test.case@email.com")
        self.test_user.save()

    def test_get_login(self):
        resp = self.test_client.get("")
        self.assertEqual(resp.status_code, 200, msg="Error in fetching login page.")

    def test_login(self):
        resp = self.test_client.post("/", {"username": self.test_user.username,
                                           "password": self.test_user.password})
        self.assertEqual(resp.status_code, 200, msg="Login failed to give a correct response status")

    def test_bad_login(self):
        resp = self.test_client.post("/", {"username": self.test_user.username,
                                           "password": "this is a bad password"})
        self.assertEqual(resp.context["message"], "Incorrect password",
                         msg="Bad password message not shown upon bad login.")

    def test_bad_username(self):
        resp = self.test_client.post("/", {"username": "bad username", "password": self.test_user.password})
        self.assertEqual(resp.context["message"], "Incorrect username",
                         msg="Bad username message does not show with incorrect username")