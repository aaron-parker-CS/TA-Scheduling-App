from django.test import TestCase, Client
from TAScheduler.models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from TAScheduler.models import User, Info


class AccountCreationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username="testuser", email="testuser@example.com",
                                                  password="testpassword123")

    def test_successful_account_creation(self):
        # Test creating an account with valid data.
        response = self.client.post('/create-account/', {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
            "phone": "1234567890",
            "address": "123 Test St",
            "type": "TA"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to create a user account.")

    def test_duplicate_username(self):
        """
        Test creating an account with a duplicate username.
        """
        User.objects.create_user(username="existinguser", password="password123")
        response = self.client.post('/create-account/', {
            "username": "existinguser",  # Duplicate username
            "password": "newpassword",
            "email": "newuser@example.com",
            "phone": "1234567890",
            "address": "123 Test St",
            "type": "TA"
        })
        self.assertIn("User already exists", response.content.decode(),
                      msg="Duplicate username should trigger an error message.")

    def test_empty_fields(self):
        """
        Test creating an account with empty required fields.
        """
        response = self.client.post('/create-account/', {
            "username": "",
            "password": "",
            "email": "",
            "phone": "",
            "address": "",
            "type": ""
        })
        self.assertIn("Enter required fields.", response.content.decode(),
                      msg="Empty required fields should trigger a validation error message.")

    def test_account_creation_with_non_duplicate_non_empty_email(self):
        response = self.client.post('/create-account/', {
            "username": "newuser",
            "password": "newpassword123",
            "email": "invalidemailformat",
            "phone": "1234567890",
            "address": "123 Test St",
            "type": "TA"
        })
        self.assertIn("Creation successful", response.content.decode(),
                      msg="Account should be created with non-empty, non-duplicate email.")

    def test_account_creation_non_empty_username(self):
        response = self.client.post('/create-account/', {
            "username": "",
            "password": "newpassword123",
            "email": "newuser@example.com",
            "phone": "1234567890",
            "address": "123 Test St",
            "type": "TA"
        })
        self.assertIn("Enter required fields.", response.content.decode(),
                      msg="Account creation with an empty username should be rejected.")

    def test_account_creation_valid_unique_username(self):
        response = self.client.post('/create-account/', {
            "username": "uniqueuser",
            "password": "newpassword123",
            "email": "uniqueuser@example.com",
            "phone": "1234567890",
            "address": "123 Test St",
            "type": "TA"
        })
        self.assertIn("Creation successful", response.content.decode(),
                      msg="Account should be created with a unique, non-empty username.")
