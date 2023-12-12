from TAScheduler.models import UserAssignment


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

