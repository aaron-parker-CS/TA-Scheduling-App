from django.shortcuts import render, redirect
from django.views import View
from .models import Course, Section, User, UserAssignment, SEMESTER_CHOICES
from django.contrib.auth import authenticate, login


# Create your views here.
class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard/')
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST["username"]
        if not User.objects.filter(username=username).exists():
            return render(request, "login.html", {"message": "Incorrect username"})
        password = request.POST["password"]
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

class createCourse(View):
    def get(self, request):
        return render(request, "createCourse.html", {"SEMESTER_CHOICES":SEMESTER_CHOICES.choices})
    def post(self, request):
        return redirect('/')
