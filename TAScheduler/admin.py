from django.contrib import admin
from TAScheduler.models import Course, Section, UserAssignment, Info, Skill, UserHasSkill

# Register your models here.
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Info)
admin.site.register(UserAssignment)
admin.site.register(Skill)
admin.site.register(UserHasSkill)
