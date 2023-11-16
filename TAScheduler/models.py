from django.db import models


# Create your models here.

class Course(models.Model):
    course_num = models.IntegerField(primary_key=True)
    semester = models.TextChoices("Semester", "SUMMER FALL SPRING WINTERIM")
    year = models.IntegerField(null=False)


class Section(models.Model):
    course_num = models.ForeignKey('Course', on_delete=models.CASCADE)
    section_num = models.IntegerField(primary_key=True)
    section_type = models.TextChoices("Section Type", "LECTURE LAB DISCUSSION")
    location = models.CharField(max_length=20, null=False)
