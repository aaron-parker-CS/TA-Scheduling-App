from TAScheduler.models import UserAssignment, Course


def auth_assignment(user, course):
    try:
        user_assignment = UserAssignment.objects.filter(user_id=user, course=course)
    except Exception as e:
        print(str(e))
        return False
    if not user_assignment.exists():
        return False
    return True


def assign_user_to_course(user, course):
    if UserAssignment.objects.filter(user_id=user, course=course).exists():
        return False
    try:
        new_assignment = UserAssignment(user_id=user, course=course)
        new_assignment.save()
        return True
    except Exception as e:
        print("THIS ERROR")
        print(e)
        return False


def assign_user_to_section(user, section):
    if user is None or section is None:
        return False

    course = Course.objects.get(id=section.course_id)
    print(f"COURSE: {course}")
    if UserAssignment.objects.filter(user_id=user, section=section, course=course).exists():
        print("HERE1")
        return False
    try:
        user_assignment = UserAssignment.objects.get(user_id=user, course=course)
        user_assignment.section = section
        user_assignment.save()
        return True
    except Exception as e:
        print("HERE1")
        print(e)
        return False

