from TAScheduler.models import Course, Section, User, UserAssignment, Info
class SectionClass():
    def populate_course_list(self):
        course_list = []
        courses = list(Course.objects.all())
        if len(courses) > len(self.course_list):
            for course in courses:
                course_list.append((course, course.__str__()))
            course_list.sort(key=str)
        return course_list

    def find_course_obj(self, course_id):
        courses = Course.objects.all()
        courseObj = None
        for i in courses:
            if str(i.__str__()) == course_id:
                courseObj = i
                break
        return courseObj