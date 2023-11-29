from django.test import TestCase, Client
from TAScheduler.models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from django.contrib.auth import authenticate

class DeleteAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Creating a user
        self.admin_user = User.objects.create_user('admin', 'admin@example.com', 'adminpassword')
        self.client.login(username='admin', password='adminpassword')

    def test_successful_delete(self):
        # Use authenticate to check if the user with the specified credentials exists
        user = authenticate(username='admin', password='adminpassword')
        self.assertIsNotNone(user, 'User authentication failed')

        response = self.client.post('/deleteAccount/', {
            "userId": user.id,
        })

        self.assertFalse(User.objects.filter(username="admin").exists(), 'Account delete unsuccessful')
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existing_user(self):
        response = self.client.post('/deleteAccount/', {
            "userId": 999,  # Some non-existent user ID
        })
        self.assertContains(response, "User not found.", msg_prefix="Incorrect message received for delete non existing user.")

    def test_unauthorized_access(self):
        # Use authenticate to check if the user with the specified credentials exists
        user = authenticate(username='admin', password='adminpassword')
        self.assertIsNotNone(user, 'User authentication failed')
        self.client.logout()
        response = self.client.post('/deleteAccount/', {
            "userId": user.id,
        })

        self.assertTrue(User.objects.filter(username="admin").exists(), "Account deleted without authorization")

    def test_confirmation(self):
        user_to_delete = User.objects.create_user('user_to_delete', 'delete@example.com', 'deletepassword')
        response = self.client.post('/deleteAccount/', {'userId': user_to_delete.id})
        self.assertContains(response, 'deleted successfully')
