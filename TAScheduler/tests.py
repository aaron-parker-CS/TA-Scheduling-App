from django.test import TestCase, Client
from .models import User, UserAssignment, Course, Section, Info


# Create your tests here.
class TestModels(TestCase):
    test_user = None
    test_section = None
    test_course = None
    test_assignment = None

    def setUp(self):
        self.test_user = User(username="test", password="pass", email="test.user@email.com")
        self.test_course = Course(course_num=351, semester="Fa", year=2023,
                                  description="Data Structures and Algorithms")
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
        self.assertEquals(resp.status_code, 200, msg="Login failed to give a correct response status")

    def test_bad_login(self):
        resp = self.test_client.post("/", {"username": self.test_user.username,
                                           "password": "this is a bad password"})
        self.assertEquals(resp.context["message"], "Incorrect password",
                          msg="Bad password message not shown upon bad login.")

    def test_bad_username(self):
        resp = self.test_client.post("/", {"username": "bad username", "password": self.test_user.password})
        self.assertEquals(resp.context["message"], "Incorrect username",
                          msg="Bad username message does not show with incorrect username")


class TestDashboard(TestCase):
    test_user = None
    test_client = None

    def setUp(self):
        self.test_client = Client()
        self.test_user = User(username="test", password="password")

    def test_no_login(self):
        # No login should redirect to the login screen
        resp = self.test_client.get("/dashboard/")
        self.assertRedirects(response=resp, expected_url='/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)


class TestNewAccount(TestCase):
    test_user = None
    user_info = None
    test_client = None

    def setUp(self):
        self.test_client = Client()
        self.test_user = User(username="test", password="password", email='test.account@email.com')
        self.user_info = Info(user=self.test_user)
        self.test_user.info.type = self.test_user.info.TYPE_CHOICES[0]
        self.test_client.login(username=self.test_user.username, password=self.test_user.password)
        self.test_user.save()
        self.user_info.save()

    def test_create_account(self):
        resp = self.test_client.post('/create-account/', {"username": "test.account", "password": "test",
                                                          'email': 'test', 'phone': 'test', 'address': 'test',
                                                          'type': 'TA'})
        self.assertEqual(resp.context["message"], 'Creation successful',
                         msg='Message not shown on account creation')
        self.assertNotEquals(None, User.objects.get(username='test.account'), msg="User account not successfully "
                                                                                  "created.")

    def test_no_admin_redirect(self):
        self.test_user.info.type = self.test_user.info.TYPE_CHOICES[2]
        resp = self.test_client.get('/create-account/')
        self.assertEqual(resp.status_code, 403, msg="Forbidden message not given to non-admin user.")

    def test_user_created_with_info(self):
        resp = self.test_client.post('/create-account/', {"username": "test.account", "password": "test",
                                                          'email': 'test', 'phone': 'test', 'address': 'test',
                                                          'type': 'TA'})
        new_id = User.objects.get(username='test.account')
        self.assertNotEquals(None, Info.objects.get(user=new_id),
                         msg="User was created without an info model assigned to it.")

    def test_user_already_exists(self):
        resp = self.test_client.post('/create-account/', {"username": self.test_user.username, "password": "test",
                                                          'email': 'test', 'phone': 'test', 'address': 'test',
                                                          'type': 'TA'})
        self.assertEqual(resp.context['message'], 'User already exists',
                         msg='Duplicate user creation does not show the proper error message')
