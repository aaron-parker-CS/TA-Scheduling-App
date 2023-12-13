from TAScheduler.models import UserAssignment, Course


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

