from django.test import TestCase
from django.urls import reverse
from TAScheduler.models import User, Info


class test_edit_info(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.info = Info.objects.create(user=self.user, phone="1234567890")
        self.client.login(username='testuser', password='testpassword')

    def test_update_with_all_fields_populated(self):
        response = self.client.post(reverse('edit-personal-info'), {
            'first-name': 'John',
            'last-name': 'Doe',
            'phone': '9876543210'})
        self.assertEqual(response.status_code, 302)

    def test_update_with_empty_skills(self):
        """
        Test updating account information with an empty skills field.
        """
        response = self.client.post(reverse('edit-personal-info'), {
            'first-name': 'Jane',
            'last-name': 'Smith',
            'phone': '1231231234'})
        self.assertEqual(response.status_code, 302)

    def test_update_with_mandatory_fields_empty(self):
        """
        Test updating account information with one of the mandatory fields empty.
        """
        response = self.client.post(reverse('edit-personal-info'), {
            'first-name': '',
            'last-name': 'Smith',
            'phone': '1231231234'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit-info.html')

    def test_no_update(self):
        """
        Test access to the update page without submitting the form.
        """
        response = self.client.get(reverse('edit-personal-info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Account Information', response.content.decode())

