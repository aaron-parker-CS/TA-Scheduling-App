from django.shortcuts import render, redirect
from django.views import View
from .models import Course, Section, User, UserAssignment, Info
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


class CreateAccount(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.info.type == 'SU':
            return render(request, 'dashboard.html', {'status_code': 403})
        return render(request, 'create-account.html', {"types": Info.TYPE_CHOICES})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return render(request, 'create-account.html', {'message': 'User already exists',
                                                           "types": Info.TYPE_CHOICES})
        new_user = User.objects.create_user(username, email, password)
        new_user.save()
        phone = request.POST['phone']
        address = request.POST['address']
        type = request.POST['type']
        info = Info(user=new_user, phone=phone, address=address, type=type)
        info.save()
        return render(request, 'create-account.html', {'message': 'Creation successful',
                                                       "types": Info.TYPE_CHOICES})



