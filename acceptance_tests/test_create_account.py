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
        response = self.client.post('/createAccount/', {
            "username": "newuser",
            "first-name": "sam",
            "last-name": "gaudet",
            "password": "newpassword",
            "phone": "1234567890",
            "type": "TA"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to create a user account.")
        self.assertEqual(response.context["message"], 'Creation successful',
                         msg='Message should have been displayed saying, "Creation successful"')
        self.assertNotEqual(None, User.objects.get(username='newuser'), msg="User account not successfully "
                                                                            "created.")

    def test_duplicate_username(self):
        """
        Test creating an account with a duplicate username.
        """
        User.objects.create_user(username="existinguser", password="password123")
        response = self.client.post('/createAccount/', {
            "username": "existinguser",  # Duplicate username
            "first-name": "sam",
            "last-name": "gaudet",
            "password": "newpassword",
            "phone": "1234567890",
            "type": "TA"
        })
        self.assertIn("User already exists", response.content.decode(),
                      msg="Duplicate username should trigger an error message.")

    def test_empty_fields(self):
        """
        Test creating an account with empty required fields.
        """
        response = self.client.post('/createAccount/', {
            "username": "",
            "first-name": "sam",
            "last-name": "gaudet",
            "password": "",
            "phone": "",
            "type": ""
        })
        self.assertIn("Enter required fields.", response.content.decode(),
                      msg="Empty required fields should trigger a validation error message.")

    def test_account_creation_with_non_duplicate_non_empty_email(self):
        response = self.client.post('/createAccount/', {
            "username": "newuser",
            "first-name": "sam",
            "last-name": "gaudet",
            "password": "newpassword123",
            "phone": "1234567890",
            "type": "TA"
        })
        self.assertIn("Creation successful", response.content.decode(),
                      msg="Account should be created with non-empty, non-duplicate email.")

    def test_account_creation_non_empty_username(self):
        response = self.client.post('/createAccount/', {
            "username": "",
            "first-name": "sam",
            "last-name": "gaudet",
            "password": "newpassword123",
            "phone": "1234567890",
            "type": "TA"
        })
        self.assertIn("Enter required fields.", response.content.decode(),
                      msg="Account creation with an empty username should be rejected.")

    def test_account_creation_valid_unique_username(self):
        response = self.client.post('/createAccount/', {
            "username": "uniqueuser",
            "first-name": "sam",
            "last-name": "gaudet",
            "password": "newpassword123",
            "phone": "1234567890",
            "type": "TA"
        })
        self.assertIn("Creation successful", response.content.decode(),
                      msg="Account should be created with a unique, non-empty username.")

    def test_user_created_with_info(self):
        response = self.client.post('/createAccount/', {
            "username": "test.account",
            "first-name": "sam",
            "last-name": "gaudet",
            "password": "test",
            'phone': 'test',
            'type': 'TA'})
        new_id = User.objects.get(username='test.account')
        self.assertNotEqual(None, Info.objects.get(user=new_id),
                            msg="User was created without an info model assigned to it.")

    def test_no_admin_redirect(self):
        self.test_user = User(username="test", password="password", email='test.account@email.com')
        self.user_info = Info(user=self.test_user)
        self.test_user.info.type = self.test_user.info.TYPE_CHOICES[0]
        self.client.login(username=self.test_user.username, password=self.test_user.password)
        self.test_user.save()
        self.user_info.save()

        self.test_user.info.type = self.test_user.info.TYPE_CHOICES[2]
        resp = self.client.get('/createAccount/')
        self.assertEqual(resp.status_code, 403, msg="Forbidden message not given to non-admin user.")
