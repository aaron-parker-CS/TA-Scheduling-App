from django.contrib.auth.models import User, AbstractUser

from TAScheduler.models import UserAssignment, Course, Section


def assign_user_to_course(user, course):
    if UserAssignment.objects.filter(user_id=user, course=course).exists():
        return False
    try:
        new_assignment = UserAssignment(user_id=user, course=course)
        new_assignment.save()
        return True
    except Exception as e:
        print(e)
        return False


def assign_user_to_section(user, section):
    if user is None or section is None:
        return False

    course = Course.objects.get(id=section.course_id)
    if UserAssignment.objects.filter(user_id=user, section=section, course=course).exists():
        return False
    try:
        new_assignment = UserAssignment(user_id=user, section=section, course=course)
        new_assignment.save()
        return True
    except Exception as e:
        print(e)
        return False


def get_sections_by_course(user: User, arr: list) -> list:
    if type(arr) is not list:
        raise ValueError('Array argument must be a list')
    if type(user) is not User:
        raise ValueError('User argument is not a Django User')
    assigned_courses = list(UserAssignment.objects.filter(user_id=user.id))
    for course in assigned_courses:
        list_sections = list(Section.objects.filter(course=course.course))
        for section in list_sections:
            arr.append(section)
    return arr

def get_users_by_course(course: Course, arr: list) -> list:
    if type(arr) is not list:
        raise ValueError('Array argument must be a list')
    if type(course) is not Course:
        raise ValueError('Course argument is not of Course type')
    assigned_courses = list(UserAssignment.objects.filter(course=course))
    for course in assigned_courses:
        arr.append(course.user_id)
    return arr