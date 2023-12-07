from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class SEMESTER_CHOICES(models.TextChoices):
    Fa = "Fall"
    Su = "Summer"
    Sp = "Spring"
    Wi = "Winterim"


class Course(models.Model):
    SEMESTER_CHOICES = [
        ('Fa', 'Fall'),
        ('Su', 'Summer'),
        ('Sp', 'Spring'),
        ('Wi', 'Winterim')
    ]

    course_num = models.IntegerField(validators=[MaxValueValidator(999), MinValueValidator(100)])
    semester = models.CharField(max_length=8, choices=SEMESTER_CHOICES, default=SEMESTER_CHOICES[0])
    year = models.IntegerField(null=False, validators=[MaxValueValidator(9999), MinValueValidator(2000)])
    description = models.CharField(max_length=500, default="", null=False)

    def __str__(self):
        return str(self.course_num) + ': ' + str(self.semester) + str(self.year)


class Section(models.Model):
    # A course has 1-to-many sections
    SECTION_CHOICES = [
        ("Lec", "LECTURE"),
        ("Lab", "LAB"),
        ("Dis", "DISCUSSION")
    ]
    course_num = models.ForeignKey('Course', on_delete=models.CASCADE)
    section_num = models.IntegerField(null=False, default=100,
                                      validators=[MaxValueValidator(999), MinValueValidator(100)])
    section_type = models.CharField(max_length=3, choices=SECTION_CHOICES)
    section_is_on_monday = models.BooleanField(null=False, default=False)
    section_is_on_tuesday = models.BooleanField(null=False, default=False)
    section_is_on_wednesday = models.BooleanField(null=False, default=False)
    section_is_on_thursday = models.BooleanField(null=False, default=False)
    section_is_on_friday = models.BooleanField(null=False, default=False)
    section_start_time = models.TimeField(null=False, default="00:00")
    section_end_time = models.TimeField(null=False, default="00:00")
    location = models.CharField(max_length=20, null=False)


class Info(models.Model):
    '''
    1-1 with the User model
    Django recommended way of extending functionality of the User model
    Usage:
        user = User.objects.get(username="fred")
        user_phone = user.Info.phone
    '''
    TYPE_CHOICES = [
        ("SU", "Supervisor"),
        ("IN", "Instructor"),
        ("TA", "Teaching Assistant")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=False, default="N/A")
    address = models.CharField(max_length=20, null=False, default="N/A")
    type = models.CharField(max_length=2, null=False, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])


class UserAssignment(models.Model):
    # M-N
    # A user may have many section assignments, a section may have more than one TA or lecturer assignment
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    section_num = models.ForeignKey(to=Section, on_delete=models.CASCADE)
