from django.test import TestCase, Client
from TAScheduler.models import User, UserAssignment, Course, Section, Info
from django.test import TestCase, Client
from TAScheduler.models import User, Info
class MyTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.client = Client()
        # Creating a user with privileges to assign courses
        self.test_user = User.objects.create_user('admin', 'admin@example.com')
        self.test_user.set_password('adminpassword')
        self.test_user.save()
        self.client.login(username='admin', password='adminpassword')
        self.client.post('/', {'username': 'admin', 'password': 'adminpassword'})

    def test_edit_info(self):
        resp = self.client.post('/editInfo/', {'first-name': 'test', 'last-name': 'mctestface', 'phone': '5555555555', 'message': ''})
        self.assertEqual('5555555555', self.test_user.info.phone,
                         msg='Edit info does not correctly update the info model')

    def test_edit_info_fname_empty(self):
        resp = self.client.post('/editInfo/', {'first-name': '', 'last-name': 'mctestface', 'phone': '5555555555',
                                               'message': ''})
        print(resp.content.decode())
        self.assertEqual(resp.context['message'], 'First name may not be empty',
                         msg='Empty message not properly displayed')

    def test_edit_info_lname_empty(self):
        resp = self.client.post('/editInfo/', {'first-name': 'test', 'last-name': '', 'phone': '5555555555',
                                               'message': ''})
        print(resp.content.decode())
        self.assertEqual(resp.context['message'], 'Last name may not be empty',
                         msg='Empty message not properly displayed')

    def test_edit_info_phone_empty(self):
        resp = self.client.post('/editInfo/', {'first-name': 'test', 'last-name': 'mctestface', 'phone': '',
                                               'message': ''})
        print(resp.content.decode())
        self.assertEqual(resp.context['message'], 'Phone may not be empty',
                         msg='Empty message not properly displayed')