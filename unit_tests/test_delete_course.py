from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, UserAssignment, Course, Section, Info, SEMESTER_CHOICES
from django.db import IntegrityError, DataError


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
