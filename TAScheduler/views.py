import logging
import string
from datetime import datetime
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from Classes.AssignUserClass import assign_user_to_course, assign_user_to_section, get_sections_by_course, \
    get_users_by_course
from Classes.AuthClass import auth_type
from Classes.CreateAccountClass import CreateAccountClass
from Classes.DashboardClass import DashboardClass
from Classes.EnterSkillClass import EnterSkillClass
from Classes.LoginClass import LoginClass
from Classes.SectionClass import SectionClass
from Classes.UpdateInfo import updateInfo

from Classes.DeleteAccountClass import DeleteAccountClass
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

        role = auth_type(request.user)
        dashboard_loader = DashboardClass()

        user_list = []
        if role == 'Teaching Assistant':
            dashboard_loader.loadTAUsers(user_list)
        else:
            dashboard_loader.loadItems(User, user_list)

        course_list = []
        dashboard_loader.loadItems(Course, course_list)

        section_list = []
        dashboard_loader.loadItems(Section, section_list)

        username = User.objects.get(username=request.user)

        return render(request, "dashboard.html", {'username': username, 'role': role,
                                                  'users': user_list, 'courses': course_list, 'sections': section_list})


class CreateAccount(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()
        return render(request, 'create-account.html', {"types": Info.TYPE_CHOICES})

    def post(self, request):
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()

        username = request.POST["username"]
        fname = request.POST['first-name']
        lname = request.POST['last-name']
        password = request.POST['password']
        phone = request.POST['phone']
        type_chosen = request.POST['type']

        try:
            cac = CreateAccountClass()
            cac.create_user(username, fname, lname, password, phone, type_chosen)

        except ValueError as e:
            return render(request, 'create-account.html', {'message': e,
                                                           "types": Info.TYPE_CHOICES})

        return render(request, 'create-account.html', {'message': 'Creation successful',
                                                       "types": Info.TYPE_CHOICES})


class createCourse(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()
        return render(request, "createCourse.html", {"SEMESTER_CHOICES": SEMESTER_CHOICES.choices})

    def post(self, request):
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()

        course_num = request.POST.get('course_num')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        description = request.POST.get('description')

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
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()

        users = User.objects.all()
        context = {"users": users}
        return render(request, "DeleteAccount.html", context)

    def post(self, request):
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()

        selected_user_id = request.POST.get('userId')
        account_manager = DeleteAccountClass()
        success_message, error_message = account_manager.delete_user(selected_user_id)

        context = {'message': success_message or error_message, 'users': User.objects.all()}
        return render(request, "DeleteAccount.html", context)


class createSection(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()

        course_list = []
        course_tool = SectionClass()
        course_list = course_tool.populate_course_list(course_list)

        context = {"courses": course_list, "types": Section.SECTION_CHOICES}
        return render(request, "create-section.html", context)

    def post(self, request):
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()

        course_list = []
        course_tool = SectionClass()
        course_list = course_tool.populate_course_list(course_list)

        course_id = request.POST.get('course_num')
        courseObj = course_tool.find_course_obj(course_id)

        section_start_time = request.POST.get('start_time')
        section_end_time = request.POST.get('end_time')
        start_time = datetime.strptime(section_start_time, '%H:%M')
        end_time = datetime.strptime(section_end_time, '%H:%M')
        is_valid_time = course_tool.validate_time(start_time, end_time)

        if not is_valid_time:
            return render(request, "create-section.html", {
                "message": "Section end time is before section begin time",
                "courses": course_list,
                "types": Section.SECTION_CHOICES
            })

        section_type = request.POST.get('type')
        section_num = request.POST.get('section')
        section_is_on_friday = request.POST.get('friday')
        section_is_on_thursday = request.POST.get('thursday')
        section_is_on_wednesday = request.POST.get('wednesday')
        section_is_on_tuesday = request.POST.get('tuesday')
        section_is_on_monday = request.POST.get('monday')

        location = request.POST.get('location')
        section_is_on_friday = False if section_is_on_friday is None else True
        section_is_on_thursday = False if section_is_on_thursday is None else True
        section_is_on_wednesday = False if section_is_on_wednesday is None else True
        section_is_on_tuesday = False if section_is_on_tuesday is None else True
        section_is_on_monday = False if section_is_on_monday is None else True

        check = Section.objects.filter(course=courseObj, section_num=section_num)
        if check.exists():
            return render(request, "create-section.html", {
                "message": "Duplicate Section Number",
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
                "message": "Duplicate Section Number",
                "courses": course_list,
                "types": Section.SECTION_CHOICES
            })
        except Exception as e:
            return render(request, "create-section.html", {
                "message": str(e),
                "courses": course_list,
                "types": Section.SECTION_CHOICES
            })


class EnterSkill(View):
    def get(self, request):
        skills = request.user.info.skills
        esc = EnterSkillClass()
        skill_list = esc.create_skill_list(skills)

        return render(request, "skills.html", {"skill_list": skill_list})

    def post(self, request):
        skill_to_add = request.POST["skills"]
        if User.Info.skills is None:
            User.Info.skills + skill_to_add
        else:
            User.Info.skills + "," + skill_to_add
        return render(request, "skills.html", {})


class assignCourse(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        if not auth_type(request.user) == 'Supervisor':
            raise PermissionDenied()
        users = User.objects.all()
        courses = Course.objects.all()
        context = {"users": users, "courses": courses}
        return render(request, "assignCourse.html", context)

    def post(self, request):
        user = User.objects.get(id=request.POST.get('userId'))
        course = Course.objects.get(id=request.POST.get('courseId'))

        if assign_user_to_course(user, course):
            return redirect('/')
        else:
            return render(request, 'assignCourse.html', {'users': User.objects.all(), 'courses': Course.objects.all(),
                                                         'message': 'Unable to assign user'})


class editInfo(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        first_name = request.user.first_name
        last_name = request.user.last_name
        phone = request.user.info.phone
        skills = request.user.info.skills
        return render(request, 'edit-info.html', {"first": first_name, "last": last_name,
                                                  "phone": phone, "skills": skills})

    def post(self, request):
        first = request.POST.get('first-name')
        last = request.POST.get('last-name')
        phone = request.POST.get('phone')
        skills = request.POST.get('skills')
        message = ''

        result = updateInfo(request.user, first, last, phone, skills, message)
        if result:
            return redirect('/')
        else:
            return render(request, 'edit-info.html', {"first": request.user.first_name, "last": request.user.last_name,
                                                      "phone": request.user.info.phone,
                                                      "skills": request.user.infoskills, 'message': message})


class assignSection(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        try:
            # Filter sections by sections assigned to user
            sections = []
            user = User.objects.get(id=request.user.id)
            sections = get_sections_by_course(user, sections)
            users = []
            assigned_courses = UserAssignment.objects.filter(user_id=user)
            for course in assigned_courses:
                users = get_users_by_course(course.course, users)

            return render(request, "assign-section.html", {"users": users, "sections": sections, "message": ""})
        except Exception as e:
            return render(request, "assign-section.html", {"users": [], "sections": [], "message": str(e)})

    def post(self, request):
        user = User.objects.get(id=request.POST.get('userId'))
        section = Section.objects.get(id=request.POST.get('sectionId'))
        if assign_user_to_section(user, section):
            return redirect('/')
        else:
            return render(request, 'assign-section.html',
                          {'users': User.objects.all(), 'sections': Section.objects.all(),
                           'message': 'Unable to assign user'})
