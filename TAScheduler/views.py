from django.shortcuts import render, redirect
from django.views import View
from .models import Course, Section, User, UserAssignment
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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Logging in " + username)
            return redirect("dashboard/", {"user": user})
        else:
            return render(request, "login.html", {"message": "bad password"})


class Dashboard(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        return render(request, "dashboard.html", {})
