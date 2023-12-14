from django.test import TestCase

from Classes.AssignUserClass import assign_user_to_course, assign_user_to_section, get_sections_by_course, \
    get_users_by_course
from TAScheduler.models import User, Info, Course, Section, UserAssignment


class TestAssignUser(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'Th1$ 1$ @ t3$t')
        self.test_user.save()
        self.test_types = Info.objects.create(user=self.test_user)
        self.test_types.save()
        self.test_course = Course(course_num=478, semester='Fa', year=2023, description='Introduction to testing')
        self.test_course.save()
        self.test_section = Section(course=self.test_course, location="EMS99")
        self.test_section.save()

    def test_assign_user_course_success(self):
        result = assign_user_to_course(self.test_user, self.test_course)
        self.assertTrue(result, 'assign course fails to return true for correct inputs')

    def test_assign_user_course_fail(self):
        result = assign_user_to_course(None, None)
        self.assertFalse(result, 'assign course fails to return false for incorrect inputs')

    def test_assign_course_twice(self):
        assign_user_to_course(self.test_user, self.test_course)
        result = assign_user_to_course(self.test_user, self.test_course)
        self.assertFalse(result, 'assign course fails to return false for duplicate course assignment')

    def test_assign_user_section_success(self):
        test_assignment = assign_user_to_course(self.test_user, self.test_course)
        result = assign_user_to_section(self.test_user, self.test_section)
        self.assertTrue(result, 'assign course fails to return true for correct inputs')

    def test_assign_user_section_fail(self):
        result = assign_user_to_section(None, None)
        self.assertFalse(result, 'assign section fails to return false for incorrect inputs')

    def test_assign_section_twice(self):
        assign_user_to_section(self.test_user, self.test_section)
        result = assign_user_to_section(self.test_user, self.test_section)
        self.assertFalse(result, 'assign section fails to return false for duplicate course assignment')

    def test_get_sections_by_course(self):
        assignment = UserAssignment(user_id=self.test_user, course=self.test_course)
        assignment.save()
        section_list = []
        section_list = get_sections_by_course(self.test_user, section_list)
        self.assertIn(self.test_section, section_list,
                      msg="Get sections by course fails to fetch the section by user assignments")

    def test_get_sections_null(self):
        with self.assertRaises(ValueError, msg='None argument fails to raise ValueError'):
            section_list = get_sections_by_course(self.test_user, None)
            section_list = get_sections_by_course(None, section_list)

    def test_get_sections_invalid(self):
        with self.assertRaises(ValueError, msg='None argument fails to raise ValueError'):
            section_list = get_sections_by_course(self.test_user, {})
            section_list = get_sections_by_course('test', section_list)

    def test_get_sections_other_course(self):
        new_course = Course(course_num=599, semester='Fa', year=2022, description='Testing')
        new_course.save()
        new_section = Section(course=new_course, section_num=400, section_type='Lec', section_is_on_monday=True,
                              section_is_on_wednesday=True,section_start_time='12:00', section_end_time='13:00',
                              location='Online')
        new_section.save()
        assignment = UserAssignment(user_id=self.test_user, course=self.test_course)
        assignment.save()
        section_list = []
        section_list = get_sections_by_course(self.test_user, section_list)
        self.assertNotIn(new_section, section_list, msg='Unrelated section shows inside of get sections by course')

    def test_get_users_by_course(self):
        assignment = UserAssignment(user_id=self.test_user, course=self.test_course)
        assignment.save()
        user_list = []
        user_list = get_users_by_course(self.test_course, user_list)
        self.assertIn(self.test_user, user_list,
                      msg="Get users by course fails to fetch the user by course assignments")

