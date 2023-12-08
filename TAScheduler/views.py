from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from Classes.CreateAccountClass import CreateAccountClass
from .models import Course, Section, User, UserAssignment, Info, SEMESTER_CHOICES
from django.contrib.auth import authenticate, login


# Create your views here.
class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard/')
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST["username"]
        if username is None or username == '':
            return render(request, 'login.html', {'message': 'This field is required.'})
        if not User.objects.filter(username=username).exists():
            return render(request, "login.html", {"message": "Incorrect username"})
        password = request.POST["password"]
        if password is None or password == '':
            return render(request, 'login.html', {'message': 'This field is required.'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Logging in " + username)
            return redirect("dashboard/", {"user": user})
        else:
            return render(request, "login.html", {"message": "Incorrect password"})


class Dashboard(View):

    def loadUsers(self, li):
        users = User.objects.all()
        header = ['Username', 'First Name', 'Last Name', 'User Type', 'Email', 'Phone Number', 'Assigned Sections',
                  'Skills']
        li.append(header)
        for user in users:
            user_attr = [user.username, user.first_name, user.last_name, user.info.type, user.email, user.info.phone]
            assigned_sections = []
            sections = UserAssignment.objects.filter(user_id=user)
            for section in sections:
                assigned_sections.append(section)

            user_attr.append(assigned_sections)
            li.append(user_attr)

    def loadCourses(self, li):
        courses = Course.objects.all().order_by('year', 'course_num', 'semester')
        header = ['Course Name', 'Course Number', 'Semester', 'Year']
        li.append(header)
        for course in courses:
            course_attr = [course.description, course.course_num, course.semester, course.year]
            li.append(course_attr)

    def loadSections(self, li):
        sections = Section.objects.all().order_by('course_num__year', 'course_num__course_num', 'course_num__semester')
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
            section_attr = [section.course_num, section.section_num, section.section_type, dayStr,
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

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')

        user_list = []
        self.loadItems(User, user_list)

        course_list = []
        self.loadItems(Course, course_list)

        section_list = []
        self.loadItems(Section, section_list)

        username = User.objects.get(username=request.user)
        role = username.info.type

        return render(request, "dashboard.html", {'username': username, 'role': role,
                                                  'users': user_list, 'courses': course_list, 'sections': section_list})


class CreateAccount(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.info.type == 'SU':
            return render(request, 'dashboard.html', status=403)
        return render(request, 'create-account.html', {"types": Info.TYPE_CHOICES})

    def post(self, request):
        username = request.POST["username"]
        email = request.POST['email']
        password = request.POST["password"]
        phone = request.POST['phone']
        address = request.POST['address']
        type_chosen = request.POST['type']

        try:
            cac = CreateAccountClass()
            cac.create_user(username, email, password, phone, address, type_chosen)

        except ValueError as e:
            return render(request, 'create-account.html', {'message': e,
                                                           "types": Info.TYPE_CHOICES})

        return render(request, 'create-account.html', {'message': 'Creation successful',
                                                       "types": Info.TYPE_CHOICES})


class createCourse(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(request, "createCourse.html", {"SEMESTER_CHOICES": SEMESTER_CHOICES.choices})

    def post(self, request):
        course_num = request.POST.get('course_num')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        description = request.POST.get('description')

        # TODO: Find a better fix. Keep in mind that these POST responses return empty strings if the textbox is
        #  empty, not None.

        if Course.objects.filter(course_num=course_num, semester=semester, year=year).exists():
            return render(request, "createCourse.html", {
                "message": "Duplicate course number. Please use a unique number.",
                "SEMESTER_CHOICES": SEMESTER_CHOICES.choices
            })

        # Creating a new course instance but not saving it yet
        new_course = Course(
            course_num=course_num,
            semester=semester,
            year=year,
            description=description
        )

        try:
            # Validate the course before saving
            new_course.full_clean()
            new_course.save()
            return redirect('/dashboard/')
        except ValidationError as ve:
            # Handle validation errors
            return render(request, "createCourse.html", {
                "message": "Validation Error: " + str(ve),
                "SEMESTER_CHOICES": SEMESTER_CHOICES.choices
            })
        except Exception as e:
            return render(request, "createCourse.html", {
                "message": str(e),
                "SEMESTER_CHOICES": SEMESTER_CHOICES.choices
            })


class DeleteAccount(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        users = User.objects.all()
        context = {"users": users}
        return render(request, "DeleteAccount.html", context)

    def post(self, request):
        selected_user_id = request.POST.get('userId')
        # delete user
        try:
            user_to_delete = User.objects.get(id=selected_user_id)
            user_to_delete.delete()
            message = f"Account '{user_to_delete.username}' deleted successfully."
        except User.DoesNotExist:
            message = "User not found."
        # Render the template with the appropriate context
        context = {'message': message, 'users': User.objects.all()}
        return render(request, "DeleteAccount.html", context)


class createSection(View):
    course_list = []

    def populate_course_list(self):
        courses = list(Course.objects.all())
        if len(courses) > len(self.course_list):
            self.course_list = []
            for course in courses:
                self.course_list.append((course, course.__str__()))
            self.course_list.sort(key=str)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')

        self.populate_course_list()

        context = {"courses": self.course_list, "types": Section.SECTION_CHOICES}
        return render(request, "create-section.html", context)

    def post(self, request):
        # function moved to new class
        # replace with SectionClass.populate_course_list(self) ***make sure self.course_list exists
        self.populate_course_list(self)
        ###
        course_id = request.POST.get('course_num')
        courses = Course.objects.all()

        #function moved to new class
        #replace w/ courseObj = SectionClass.find_course_obj(self,course_id)
        courseObj = None
        for i in courses:
            if str(i.__str__()) == course_id:
                courseObj = i
                break
        ###
        section_type = request.POST.get('type')
        print(section_type)
        section_num = request.POST.get('section')
        section_is_on_friday = request.POST.get('friday')
        section_is_on_thursday = request.POST.get('thursday')
        section_is_on_wednesday = request.POST.get('wednesday')
        section_is_on_tuesday = request.POST.get('tuesday')
        section_is_on_monday = request.POST.get('monday')
        section_start_time = request.POST.get('start_time')
        section_end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        section_is_on_friday = False if section_is_on_friday is None else True
        section_is_on_thursday = False if section_is_on_thursday is None else True
        section_is_on_wednesday = False if section_is_on_wednesday is None else True
        section_is_on_tuesday = False if section_is_on_tuesday is None else True
        section_is_on_monday = False if section_is_on_monday is None else True
        # new_section = None
        # try:
        #     if courseObj is not None:
        #         sections = Section.objects.filter(course_num=courseObj)
        #
        #     for course in self.course_list:
        #         if course[1] == courseObj.__str__():
        #             for j in sections:
        #                 if j.section_num == courseObj.section_num:
        #                     print("Duplicate")
        #                     return render(request, "create-section.html",
        #                               {"courses": self.course_list, "message": "Duplicate Course Number"})
        # except AttributeError as z:
        #     print(z)
        #     return render(request, "create-section.html",
        #                   {"courses": self.course_list, "message": "Duplicate Course Number"})

        check = Section.objects.filter(course_num=courseObj, section_num=section_num)
        if check.exists():
            return render(request, "create-section.html", {
                "message": "Duplicate Course Number",
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })

        new_section = Section(
            course_num=courseObj,
            section_num=section_num,
            section_type=section_type,
            section_is_on_friday=section_is_on_friday,
            section_is_on_thursday=section_is_on_thursday,
            section_is_on_wednesday=section_is_on_wednesday,
            section_is_on_tuesday=section_is_on_tuesday,
            section_is_on_monday=section_is_on_monday,
            section_start_time=section_start_time,
            section_end_time=section_end_time,
            location=location)

        try:
            # Validate the section before saving
            new_section.full_clean()
            new_section.save()
            return render(request, "create-section.html", {
                "message": 'Creation successful',
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })
        except ValidationError as ve:
            # Handle validation errors
            print(f"Validation Error: {ve.message_dict}")
            return render(request, "create-section.html", {
                "message": "Validation Error",
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })
        except IntegrityError:
            return render(request, "create-section.html", {
                "message": "Duplicate Course Number",
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })
        except Exception as e:
            return render(request, "create-section.html", {
                "message": str(e),
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })
