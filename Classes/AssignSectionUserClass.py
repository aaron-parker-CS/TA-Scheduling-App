from TAScheduler.models import Course, Section, User, UserAssignment, Info
class AssignSectionClass():
    def find_section(self, section_id):
        sectionObj = []
        sections = Section.objects.all()

        for section in sections:
            if section.__str__() == section_id:
                sectionObj = section

        return sectionObj

    def find_user(self, user_name):
        userObj = []
        users = User.objects.all()

        for user in users:
            if user.username == user_name:
                userObj = user

        return userObj