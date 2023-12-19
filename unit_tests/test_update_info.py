from django.test import TestCase
from TAScheduler.models import User, Info

from Classes.UpdateInfo import updateInfo


class TestUpdateInfo(TestCase):
    def setUp(self):
        self.test_user = User(username='testmctestface1', email='testmctestface@uwm.edu', password='passmcpassface')
        self.test_user.save()
        self.test_info = Info(user=self.test_user, phone='N/A',type='SU')
        self.test_info.save()

    def test_update_success(self):
        result = updateInfo(self.test_user, 'test', 'mctestface', '555-5555', '')
        self.assertEqual('True', result, 'updateInfo fails to return True for valid input.')

    def test_update_missing_info(self):
        result = updateInfo(self.test_user, '', '', '', '')
        self.assertEqual('First name may not be empty', result, 'updateInfo fails to return false for invalid input.')

    def testing_update_null_info(self):
        result = updateInfo(self.test_user, None, None, None, None)
        self.assertEqual('First name may not be empty', result, 'updateInfo fails to return false for null input.')

    def testing_update_no_user(self):
        result = updateInfo(None, 'test', 'mctestface', '555-5555', '')
        self.assertEqual('User may not be empty', result, 'updateInfo fails to return false with no user.')
