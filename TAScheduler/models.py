from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Course(models.Model):
    SEMESTER_CHOICES = [
        ("Fa", "FALL"),
        ("Su", "SUMMER"),
        ("Sp", "SPRING"),
        ("Wi", "WINTERIM")
    ]
    course_num = models.IntegerField(primary_key=True)
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    year = models.IntegerField(null=False)


class Section(models.Model):
    # A course has 1-to-many sections
    SECTION_CHOICES = [
        ("Lec", "LECTURE"),
        ("Lab", "LAB"),
        ("Dis", "DISCUSSION")
    ]
    course_num = models.ForeignKey('Course', on_delete=models.CASCADE)
    section_num = models.IntegerField(primary_key=True)
    section_type = models.CharField(max_length=3, choices=SECTION_CHOICES)
    section_is_on_monday = models.BooleanField(null=False)
    section_is_on_tuesday = models.BooleanField(null=False)
    section_is_on_wednesday = models.BooleanField(null=False)
    section_is_on_thursday = models.BooleanField(null=False)
    section_is_on_friday = models.BooleanField(null=False)
    section_start_time = models.TimeField(null=False)
    section_end_time = models.TimeField(null=False)
    location = models.CharField(max_length=20, null=False)


class UserAssignment(models.Model):
    # M-N
    # A user may have many section assignments, a section may have more than one TA or lecturer assignment
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    section_num = models.ForeignKey('Section', on_delete=models.CASCADE)
