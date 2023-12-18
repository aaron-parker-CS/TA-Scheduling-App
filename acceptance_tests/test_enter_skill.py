from django.contrib.auth.models import User
from django.test import TestCase, Client

from TAScheduler.models import UserHasSkill, Skill


class TestEnterSkill(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username="TA", email="testuser@example.com",
                                                  password="tapassword")
        self.client.login(username='TA', password='tapassword')

    #test for successful add
    def test_successful(self):
        response = self.client.post('/enterSkill/', {"skills": "Java"})

        self.assertContains(response, "Skill Added")

    #test for blank
    def test_blank(self):
        response = self.client.post('/enterSkill/', {"skills": ""})

        self.assertContains(response, "Line was blank")

    #test for duplicate
    def test_duplicate(self):
        self.Skill = Skill.objects.create(skill="Java")
        self.UserHasSkill = UserHasSkill.objects.create(skill=self.Skill, user=self.test_user)
        self.Skill.save()
        self.UserHasSkill.save()
        response = self.client.post('/enterSkill/', {"skills": "Java"})

        self.assertContains(response, "You already have this skill")

    #test for a space
    def test_space(self):
        response = self.client.post('/enterSkill/', {"skills": "Java "})

        self.assertContains(response, "Please enter one word(ex: Python)")
