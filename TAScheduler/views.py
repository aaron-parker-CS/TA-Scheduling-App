from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

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

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(request, "dashboard.html", {})


class CreateAccount(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.info.type == 'SU':
            return render(request, 'dashboard.html', status=403)
        return render(request, 'create-account.html', {"types": Info.TYPE_CHOICES})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return render(request, 'create-account.html', {'message': 'User already exists',
                                                           "types": Info.TYPE_CHOICES})
        try:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
        except ValueError:
            return render(request, 'create-account.html', {'message': 'Enter required fields.',
                                                           'types': Info.TYPE_CHOICES})
        phone = request.POST['phone']
        address = request.POST['address']
        type_chosen = request.POST['type']
        info = Info(user=new_user, phone=phone, address=address, type=type_chosen)
        info.save()
        return render(request, 'create-account.html', {'message': 'Creation successful',
                                                       "types": Info.TYPE_CHOICES})


class createCourse(View):
    def get(self, request):
        return render(request, "createCourse.html", {"SEMESTER_CHOICES": SEMESTER_CHOICES.choices})

    def post(self, request):
        course_num = request.POST.get('course_num')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        description = request.POST.get('description')
        credits = request.POST.get('credits')

        # TODO: Find a better fix. Keep in mind that these POST responses return empty strings if the textbox is
        #  empty, not None.
        credits = 1 if credits == '' or credits is None else credits

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
            credits=credits,
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
        users = User.objects.all()
        context = {"users": users}
        return render(request, "DeleteAccount.html", context)


class createSection(View):
    course_list = []

    def get(self, request):
        courses = list(Course.objects.all())

        self.course_list = []
        
        for course in courses:
            self.course_list.append((course, course.__str__()))

        context = {"courses": self.course_list, "types": Section.SECTION_CHOICES}
        return render(request, "create-section.html", context)

    def post(self, request):
        courses = Course.objects.all()
        course_num = request.POST.get('course_num')

        course = None
        for item in courses:
            if item.__str__() == course_num:
                course = item

        section_type = request.POST.get('type')
        section_num = request.POST.get('section')
        section_is_on_friday = request.POST.get('friday')
        section_is_on_thursday = request.POST.get('thursday')
        section_is_on_wednesday = request.POST.get('wednesday')
        section_is_on_tuesday = request.POST.get('tuesday')
        section_is_on_monday = request.POST.get('monday')
        section_start_time = request.POST.get('start_time')
        section_end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        # create section object
        section_is_on_friday = False if section_is_on_friday is None else True
        section_is_on_thursday = False if section_is_on_thursday is None else True
        section_is_on_wednesday = False if section_is_on_wednesday is None else True
        section_is_on_tuesday = False if section_is_on_tuesday is None else True
        section_is_on_monday = False if section_is_on_monday is None else True

        new_section = Section(course_num=course,
                              section_num=section_num,
                              section_type=section_type, section_is_on_friday=section_is_on_friday,
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
            return render(request, "create-section.html", {
                "message": "Validation Error: " + str(ve),
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })
        except IntegrityError:
            return render(request, "create-section.html", {
                "message": "Duplicate section number. Please use a unique number.",
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })
        except Exception as e:
            return render(request, "create-section.html", {
                "message": str(e),
                "courses": self.course_list,
                "types": Section.SECTION_CHOICES
            })
