from django.test import TestCase, Client
from .models import User, UserAssignment, Course, Section


# Create your tests here.
class TestModels(TestCase):
    test_user = None
    test_section = None
    test_course = None
    test_assignment = None

    def setUp(self):
        self.test_user = User(username="test", password="pass", email="test.user@email.com")
        self.test_course = Course(course_num=351, semester="Fa", year=2023)

        self.test_section = Section(course_num=self.test_course, section_num=401, section_type="Lec",
                                    section_is_on_monday=True, section_is_on_wednesday=True, section_start_time="09:30",
                                    section_end_time="10:30", location="EMS180")
        self.test_assignment = UserAssignment(user_id=self.test_user, section_num=self.test_section)

    def test_delete_user(self):
        User.objects.filter(id=self.test_user.id).delete()
        self.assertEqual(None, self.test_assignment.id,
                         msg="Test assignment fails to delete upon user deletion, no cascades")

    def test_delete_course(self):
        Course.objects.filter(course_num=self.test_course.course_num).delete()
        self.assertEqual(None, self.test_section.id,
                         "Section fails to cascade the delete upon course deletion.")
        self.assertEqual(None, self.test_assignment.id,
                         "Assignment fails to cascade delete upon course deletion.")

    def test_delete_section(self):
        Section.objects.filter(id=self.test_section.id).delete()
        self.assertEqual(None, self.test_assignment.id,
                         "Assignment fails to cascade delete upon section deletion.")
        self.assertNotEquals(None, self.test_course.course_num, "Course deletes upon selection deletion.")


class TestLogin(TestCase):
    test_user = None
    test_client = None

    def setUp(self):
        self.test_client = Client()
        self.test_user = User(username="test", password="password", email="test.case@email.com")
        self.test_user.save()

    def test_get_login(self):
        resp = self.test_client.get("")
        self.assertEqual(resp.status_code, 200, msg="Error in fetching login page.")

    def test_login(self):
        resp = self.test_client.post("/", {"username": self.test_user.username,
                                           "password": self.test_user.password})
        self.assertRedirects(response=resp, expected_url='/dashboard/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True,
                             msg="Login POST does not properly redirect the user.")

    def test_bad_login(self):
        resp = self.test_client.post("/", {"username": self.test_user.username,
                                           "password": "this is a bad password"})
        self.assertIn("bad password", resp.body, msg="Bad password message not shown upon bad login.")

