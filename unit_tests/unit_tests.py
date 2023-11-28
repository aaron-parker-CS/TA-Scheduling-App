from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


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

    def test_null_values(self):
        resp = self.test_client.post('/create-account/', {"username": '', "password": '', 'email': 'test',
                                                          'phone': 'test', 'type': 'TA'})
        self.assertEqual(resp.context['message'], 'Enter required fields.',
                         msg='Null required values do not show the required error message.')


class CreateCourseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_course_success(self):
        """
        Test successful creation of a course through POST request
        """
        response = self.client.post('/dashboard/createCourse/', {
            'course_num': 101,
            'semester': SEMESTER_CHOICES.Fa,
            'year': 2023,
            'credits': 3,
            'description': "Intro to Testing"
        })
        self.assertEqual(response.status_code, 302, msg="Failed to create a course successfully.")
        self.assertTrue(Course.objects.filter(course_num=101).exists(), msg="Course does not exist in the database.")

    def test_course_number_validation(self):
        """
        Test course number validation (must be between 100 and 999) through POST request
        """
        response = self.client.post('/dashboard/createCourse/', {
            'course_num': 99,  # Invalid course number
            'year': 2023,
            'credits': 3
        })
        self.assertNotEqual(response.status_code, 404, msg="Expected a different status code.")
        self.assertFalse(Course.objects.filter(course_num=99).exists(), msg="Course with invalid number exists.")

    def test_course_number_validation_high(self):
        """
        Test course number validation for a number too high.
        """
        response = self.client.post('/dashboard/createCourse/', {
            'course_num': 1000,  # Invalid course number
            'year': 2023,
            'credits': 3,
            'description': "Test Course High Number"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to handle high course number properly.")
        self.assertFalse(Course.objects.filter(course_num=1000).exists(), msg="Course with high number exists.")

    def test_year_validation_low(self):
        """
        Test year validation for a year too low (before 2000).
        """
        response = self.client.post('/dashboard/createCourse/', {
            'course_num': 106,
            'semester': SEMESTER_CHOICES.Fa,
            'year': 1999,  # Invalid year
            'credits': 3,
            'description': "Test Course Early Year"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to handle low year properly.")
        self.assertFalse(Course.objects.filter(course_num=106).exists(), msg="Course with early year exists.")

    def test_year_validation_high(self):
        """
        Test year validation for a year too high (after 9999).
        """
        response = self.client.post('/dashboard/createCourse/', {
            'course_num': 107,
            'semester': SEMESTER_CHOICES.Fa,
            'year': 10000,  # Invalid year
            'credits': 3,
            'description': "Test Course Future Year"
        })
        self.assertEqual(response.status_code, 200, msg="Failed to handle high year properly.")
        self.assertFalse(Course.objects.filter(course_num=107).exists(), msg="Course with future year exists.")

    def test_credits_default_value(self):
        """
        Test that the default value of credits is 1 if not specified.
        """
        response = self.client.post('/dashboard/createCourse/', {
            'course_num': 108,
            'semester': SEMESTER_CHOICES.Fa,
            'year': 2023,
            'description': "Test Course Default Credits"
        })
        self.assertEqual(response.status_code, 302, msg="Failed to set default credits value.")
        self.assertTrue(Course.objects.filter(course_num=108, credits=1).exists(),
                        msg="Course with default credits does not exist.")

    def test_duplicate_course_number(self):
        """
        Test that creating a course with a duplicate course number through POST request is handled
        """
        self.client.post('/dashboard/createCourse/', {'course_num': 104, 'year': 2023, 'credits': 3})
        response = self.client.post('/dashboard/createCourse/', {'course_num': 104, 'year': 2024, 'credits': 4})
        self.assertNotEqual(response.status_code, 404,
                            msg="Expected a different status code for duplicate course number.")


class DeleteCourseTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(course_num=101, semester='Fa', year=2023, credits=3,
                                            description='Test Course')
        self.delete_course_url = reverse('delete_course', args=[self.course.pk])

    def test_delete_course_success(self):
        response = self.client.post(self.delete_course_url)
        self.assertEqual(response.status_code, 302, msg="Failed to delete a course.")
        self.assertFalse(Course.objects.filter(course_num=101).exists(), msg="Course still exists after deletion.")

    def test_delete_nonexistent_course(self):
        non_existent_course_pk = 9999
        delete_non_existent_course_url = reverse('delete_course', args=[non_existent_course_pk])
        response = self.client.post(delete_non_existent_course_url)
        self.assertEqual(response.status_code, 404, msg="Expected a 404 response for deleting a nonexistent course.")

    def test_redirect_after_deletion(self):
        response = self.client.post(self.delete_course_url)
        self.assertRedirects(response, reverse('dashboard-view'), status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_delete_course_count(self):
        initial_course_count = Course.objects.count()
        response = self.client.post(self.delete_course_url)
        final_course_count = Course.objects.count()
        self.assertEqual(final_course_count, initial_course_count - 1,
                         msg="Course count did not decrease after deletion.")

    def test_course_not_found_after_deletion(self):
        response = self.client.post(self.delete_course_url)
        self.assertFalse(Course.objects.filter(id=self.course.pk).exists(),
                         msg="Course should not exist after deletion.")