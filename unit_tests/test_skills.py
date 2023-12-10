from unittest import TestCase
from Classes.EnterSkillClass import EnterSkillClass


class TestCreateSkillList(TestCase):

    def setUp(self):
        self.skill_class = EnterSkillClass()

    def test_empty_skills(self):
        li = self.skill_class.create_skill_list("")
        print("Current List: " + str(li))

        self.assertEqual(1, len(li), msg="Failed to create an empty list")

    def test_one_skill(self):
        li = self.skill_class.create_skill_list("Python")
        print("Current List: " + str(li))

        self.assertEqual(1, len(li), msg="Failed to create a list with one element")

    def test_two_skills(self):
        li = self.skill_class.create_skill_list("Python,Github")
        print("Current List: " + str(li))

        self.assertEqual(2, len(li), msg="Failed to create a list with two elements")

    def test_three_skills(self):
        li = self.skill_class.create_skill_list("Python,Github,Java")
        print("Current List: " + str(li))

        self.assertEqual(3, len(li), msg="Failed to create a list with three elements")

    def test_four_skills(self):
        li = self.skill_class.create_skill_list("Python,Github,Java,Scrum")
        print("Current List" + str(li))

        self.assertEqual(4, len(li), msg="Failed to create a list with four elements")

    def test_contains_proper_word(self):
        li = self.skill_class.create_skill_list("Python")
        print("Current List: " + str(li))

        self.assertEqual("Python", li[0], msg="The String entered does not match the String found")

    def test_contains_proper_word_two_words(self):
        li = self.skill_class.create_skill_list("Python,Github")
        print("Current List: " + str(li))

        self.assertEqual("Github", li[1], msg="The String entered does not match the String found")

