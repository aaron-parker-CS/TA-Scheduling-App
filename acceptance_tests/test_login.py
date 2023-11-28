from django.test import TestCase, Client
from TAScheduler.models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from TAScheduler.models import User, Info


class LoginAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username="testuser", email="testuser@example.com",
                                                  password="testpassword123")

    def test_successful_login(self):
        """
        Test a user logging in with correct credentials.
        """
        response = self.client.post("/", {"username": "testuser", "password": "testpassword123"})
        self.assertRedirects(response, '/dashboard/',
                             msg_prefix="User should be redirected to dashboard after successful login.")

    def test_unsuccessful_login_wrong_password(self):
        """
        Test login with the correct username but wrong password.
        """
        response = self.client.post("/", {"username": "testuser", "password": "wrongpassword"})
        self.assertIn("Incorrect password", response.content.decode(),
                      msg="Incorrect password message should be displayed.")

    def test_unsuccessful_login_wrong_username(self):
        """
        Test login with the wrong username.
        """
        response = self.client.post("/", {"username": "wrongusername", "password": "testpassword123"})
        self.assertIn("Incorrect username", response.content.decode(),
                      msg="Incorrect username message should be displayed.")

    def test_unsuccessful_login_empty_fields(self):
        """
        Test login with empty username and password fields.
        """
        response = self.client.post("/", {"username": "", "password": ""})
        # You may need to adjust the expected message based on your application's validation messages.
        self.assertEquals("This field is required.", response.context['message'],
                      msg="Validation error for empty fields should be displayed.")