from django.test import TestCase

from Classes.AssignSectionUserClass import AssignSectionClass
from TAScheduler.models import User, Info, Course, Section
class TestAssignSection(TestCase):
    def setUp(self):
        self.course = Course(course_num=101, semester='Fa', year=2023,
                             description='VERIFY123')
        self.course.save()
        self.section = Section(section_num=399,
                               section_type="Dis",
                               course=self.course,
                               section_start_time="00:00:00",
                               section_end_time="00:00:01",
                               section_is_on_tuesday=True,
                               location="EMS")
        self.section.save()
        self.user = User.objects.create_user(username="test_user",
                                   password="Popthelock#",
                                   email="test@mail.com")
        self.user.save()
        self.assignSectionHelper = AssignSectionClass

    def test_find_section(self):
        # Assuming self.section is a Section model instance you expect to find
        section_id = self.section.__str__()
        sectionObj = self.assignSectionHelper.find_section(self, section_id)
        self.assertEqual(sectionObj, self.section)

    def test_find_user(self):
        user_id = self.user.username
        userObj = self.assignSectionHelper.find_user(self,user_id)
        self.assertEqual(userObj, self.user)