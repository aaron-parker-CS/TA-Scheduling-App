from django.contrib.auth.models import User
from django.test import TestCase, Client

from TAScheduler.models import UserHasSkill


class TestEnterSkill(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username="testuser", email="testuser@example.com",
                                                  password="testpassword123")
        self.UserHasSkill = UserHasSkill.objects.create(skill="", user=self.test_user)

    #test for successful add

    #test for blank

    #test for duplicate

    #test for a space
    def test_one_skill(self):
        response = self.client.post('/EnterSkill/', {"Python"})

        self.assertIn("Python", response.content.decode())
