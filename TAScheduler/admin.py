from django.contrib import admin
from TAScheduler.models import Course
from TAScheduler.models import Section
from TAScheduler.models import UserAssignment

# Register your models here.
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserAssignment)