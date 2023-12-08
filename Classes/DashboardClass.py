from TAScheduler.models import Course, Section, User, UserAssignment, Info

class DashboardClass():
    def loadUsers(self, li):
        users = User.objects.all()
        header = ['Username', 'First Name', 'Last Name', 'User Type', 'Email', 'Phone Number', 'Skills',
                  'Assigned Sections',]
        li.append(header)
        for user in users:
            if not Info.objects.filter(user=user).exists():
                user_info = Info.objects.create(user=user)
                user_info.save()

            user_type = None
            for entry in Info.TYPE_CHOICES:
                if user.info.type == entry[0]:
                    user_type = entry[1]


            user_attr = [user.username, user.first_name, user.last_name, user_type, user.email, user.info.phone, user.info.skills]
            assigned_sections = []
            sections = UserAssignment.objects.filter(user_id=user)
            for section in sections:
                assigned_sections.append(section)

            user_attr.append(assigned_sections)
            li.append(user_attr)
        return li

    def loadCourses(self, li):
        courses = Course.objects.all().order_by('year', 'course_num', 'semester')
        header = ['Course Name', 'Course Number', 'Semester', 'Year']
        li.append(header)
        for course in courses:
            course_attr = [course.description, course.course_num, course.semester, course.year]
            li.append(course_attr)

    def loadSections(self, li):
        sections = Section.objects.all().order_by('course__year', 'course__course_num', 'course__semester')
        header = ['Course', 'Section Number', 'Section Type', 'Days', 'Start Time', 'End Time']
        li.append(header)
        for section in sections:
            dayStr = ''
            if section.section_is_on_monday:
                dayStr += 'M'
            if section.section_is_on_tuesday:
                dayStr += 'T'
            if section.section_is_on_wednesday:
                dayStr += 'W'
            if section.section_is_on_thursday:
                dayStr += 'U'
            if section.section_is_on_friday:
                dayStr += 'F'
            section_attr = [section.course, section.section_num, section.section_type, dayStr,
                            section.section_start_time, section.section_end_time]
            li.append(section_attr)

    def loadItems(self, model, li):
        if model == User:
            self.loadUsers(li)
            return
        if model == Course:
            self.loadCourses(li)
            return
        if model == Section:
            self.loadSections(li)
            return

        objects = model.objects.all()
        for item in objects:
            li.append(item)