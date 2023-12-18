from TAScheduler.models import UserHasSkill, Skill


class EnterSkillClass:

    def create_skill_list(self, skills):
        skill_list = []
        if not skills.isspace():
            comma_index = skills.find(",")
            if comma_index == -1:
                skill_list.insert(0, str(skills))
            else:
                start = 0
                while comma_index != -1:
                    skill_list.insert(0, str(skills[start:comma_index]))
                    start = comma_index + 1
                    comma_index = skills.find(",", start)
                skill_list.append(skills[start:])
        # skill_list = []
        # if not skills.isspace():
        #     skill_list = skills.split(",")

        return skill_list

    def load_skills(self, user):
        skill_list = []
        skill_assignments = UserHasSkill.objects.filter(user=user)
        for assignment in skill_assignments:
            skill_list.append(assignment.skill)

        return skill_list

    def add_skill(self, user, skill_to_add):
        if skill_to_add == "":
            raise ValueError("Line was blank")

        if " " in str(skill_to_add):
            raise ValueError("Please enter one word(ex: Python)")

        skills = None
        if Skill.objects.filter(skill=skill_to_add).exists():
            skills = Skill.objects.get(skill=skill_to_add)
        else:
            skills = Skill.objects.create(skill=skill_to_add)
            skills.save()

        user_assignment = None
        if UserHasSkill.objects.filter(skill=skills).exists():
            return False
        else:
            user_assignment = UserHasSkill.objects.create(user=user, skill=skills)
            user_assignment.save()

        return True
