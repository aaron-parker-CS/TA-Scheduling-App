from django.test import TestCase, Client
from .models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from .models import User, Info


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
        self.assertIn("This field is required.", response.content.decode(),
                      msg="Validation error for empty fields should be displayed.")


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
