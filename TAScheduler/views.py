from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from Classes.CreateAccountClass import CreateAccountClass
from Classes.DashboardClass import DashboardClass
from Classes.LoginClass import LoginClass
from Classes.SectionClass import SectionClass
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
        password = request.POST["password"]
        login_validator = LoginClass()

        validation = login_validator.validate_login_fields(request, username, password)
        if validation == 'Success':
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("dashboard/", {})
        else:
            return render(request, 'login.html', {'message': validation})


class Dashboard(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')

        dashboard_loader = DashboardClass()

        user_list = []
        dashboard_loader.loadItems(User, user_list)

        course_list = []
        dashboard_loader.loadItems(Course, course_list)

        section_list = []
        dashboard_loader.loadItems(Section, section_list)

        username = User.objects.get(username=request.user)
        login_validator = LoginClass()
        role = login_validator.auth_type(request.user)

        return render(request, "dashboard.html", {'username': username, 'role': role,
                                                  'users': user_list, 'courses': course_list, 'sections': section_list})


class CreateAccount(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.info.type == 'SU':
            return render(request, 'dashboard.html', status=403)
        return render(request, 'create-account.html', {"types": Info.TYPE_CHOICES})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST['password']
        fname = request.POST['first-name']
        lname = request.POST['last-name']
        phone = request.POST['phone']
        type_chosen = request.POST['type']

        try:
            cac = CreateAccountClass()
            cac.create_user(username, password, fname, lname, phone, type_chosen)

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

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        course_list = []
        course_tool = SectionClass()
        course_list = course_tool.populate_course_list(course_list)

        context = {"courses": course_list, "types": Section.SECTION_CHOICES}
        return render(request, "create-section.html", context)

    def post(self, request):
        course_list = []
        course_tool = SectionClass()
        course_list = course_tool.populate_course_list(course_list)

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

        check = Section.objects.filter(course=courseObj, section_num=section_num)
        if check.exists():
            return render(request, "create-section.html", {
                "message": "Duplicate Course Number",
                "courses": course_list,
                "types": Section.SECTION_CHOICES
            })

        new_section = Section(
            course=courseObj,
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
            return redirect('/dashboard/')
        except ValidationError as ve:
            # Handle validation errors
            print(f"Validation Error: {ve.message_dict}")
            return render(request, "create-section.html", {
                "message": "Validation Error",
                "courses": course_list,
                "types": Section.SECTION_CHOICES
            })
        except IntegrityError:
            return render(request, "create-section.html", {
                "message": "Duplicate Course Number",
                "courses": course_list,
                "types": Section.SECTION_CHOICES
            })
        except Exception as e:
            return render(request, "create-section.html", {
                "message": str(e),
                "courses": course_list,
                "types": Section.SECTION_CHOICES
            })
