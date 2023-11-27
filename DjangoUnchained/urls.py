"""
URL configuration for DjangoUnchained project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from DjangoUnchained import settings
from TAScheduler.views import Home, Dashboard, CreateAccount, createCourse, createSection
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="main-view"),
    path('dashboard/', Dashboard.as_view(), name="dashboard-view"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('create-account/', CreateAccount.as_view(), name='create-account-view'),
    path('dashboard/createCourse/', createCourse.as_view(), name="createCourse-view"),
    path('dashboard/createSection/', createSection.as_view(), name="createSection-view")
]
