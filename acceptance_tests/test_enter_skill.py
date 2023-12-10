from django.test import TestCase, Client


class TestEnterSkill(TestCase):

    def setUp(self):
        self.client = Client()

    def test_one_skill(self):
        response = self.client.post('/EnterSkill/', {"Python"})

        self.assertIn("Python", response.content.decode())
