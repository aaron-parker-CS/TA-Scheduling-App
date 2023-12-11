from django.test import TestCase
from Classes.DeleteAccountClass import DeleteAccountClass
from TAScheduler.models import User, Info


class test_delete_account(TestCase):
    test_user = None
    delete_account_manager = None

    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'password123')
        self.test_user.save()
        self.delete_account_manager = DeleteAccountClass()

    def test_delete_existing_user(self):
        success_message, error_message = self.delete_account_manager.delete_user(self.test_user.id)
        self.assertEqual(success_message, "Account 'test' deleted successfully.", msg="Failed to delete existing user")
        self.assertIsNone(error_message, msg="Error message should be None for successful deletion")

    def test_delete_non_existing_user(self):
        non_existing_user_id = 9999  # Assuming this ID does not exist
        success_message, error_message = self.delete_account_manager.delete_user(non_existing_user_id)
        self.assertIsNone(success_message, msg="Success message should be None for non-existing user")
        self.assertIsNotNone(error_message, msg="Error message should not be None for non-existing user")
