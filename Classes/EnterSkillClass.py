class EnterSkillClass:

    def create_skill_list(self, skills):
        skill_list = []
        if not skills.isspace():
            comma_index = skills.find(",")
            if comma_index == -1:
                skill_list.append(skills)
            else:
                start = 0
                while comma_index != -1:
                    skill_list.append(skills[start:comma_index])
                    start = comma_index+1
                    comma_index = skills.find(",", start)
                skill_list.append(skills[start:])

        return skill_list
