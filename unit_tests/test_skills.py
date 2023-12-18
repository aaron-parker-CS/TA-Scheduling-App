from django.contrib.auth.models import User
from django.test import TestCase

from Classes.EnterSkillClass import EnterSkillClass
from TAScheduler.models import Skill, UserHasSkill


class TestLoadSkills(TestCase):
    def setUp(self):
        self.skill_class = EnterSkillClass()
        self.user = User.objects.create_user(username="test", email="test", password="test")
        self.user.save()
        self.Skill = Skill.objects.create(skill="Java")
        self.Skill.save()
        self.UserHasSkill = UserHasSkill.objects.create(skill=self.Skill, user=self.user)
        self.UserHasSkill.save()
        self.Skill2 = Skill.objects.create(skill="Python")
        self.Skill.save()

    def test_one_skill(self):
        li = self.skill_class.load_skills(self.user)
        self.assertEqual(1, len(li), msg="Failed to create a list with one element")
        self.assertEqual("Java", str(li[0]))

    def test_one_skill_contents(self):
        li = self.skill_class.load_skills(self.user)
        self.assertEqual("Java", str(li[0]))

    def test_two_skills(self):
        self.UserHasSkill = UserHasSkill.objects.create(skill=self.Skill2, user=self.user)
        self.UserHasSkill.save()

        li = self.skill_class.load_skills(self.user)
        self.assertEqual(2, len(li), msg="Failed to create a list with two elements")

    def test_two_skills_contents(self):
        self.UserHasSkill = UserHasSkill.objects.create(skill=self.Skill2, user=self.user)
        self.UserHasSkill.save()

        li = self.skill_class.load_skills(self.user)
        self.assertEqual("Python", str(li[1]), msg="Failed to create a list with two elements")


class TestAddSkill(TestCase):
    def setUp(self):
        self.skill_class = EnterSkillClass()
        self.user = User.objects.create_user(username="test", email="test", password="test")
        self.user.save()
        self.Skill = Skill.objects.create(skill="Java")
        self.Skill.save()
        self.UserHasSkill = UserHasSkill.objects.create(skill=self.Skill, user=self.user)
        self.UserHasSkill.save()
        self.Skill2 = Skill.objects.create(skill="Python")
        self.Skill.save()

    def test_add_success(self):
        self.skill_to_add = Skill.objects.create(skill="test")
        self.assertTrue(self.skill_class.add_skill(self.user, self.skill_to_add))

    def test_add_duplicate(self):
        self.assertFalse(self.skill_class.add_skill(self.user, self.Skill))

    def test_add_nothing(self):
        with self.assertRaises(ValueError):
            self.skill_class.add_skill(self.user, "")


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
