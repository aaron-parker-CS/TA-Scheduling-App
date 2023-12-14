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


def get_sections_by_course(user, arr):
    assigned_courses = list(UserAssignment.objects.filter(user_id=user.id))
    for course in assigned_courses:
        list_sections = list(Section.objects.filter(course=course.course))
        for section in list_sections:
            arr.append(section)
    return arr
