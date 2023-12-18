from TAScheduler.models import User, Info


def auth_type(user):

    if not Info.objects.filter(user=user).exists():
        new_info = Info.objects.create(user=user)
        new_info.save()

    role = None
    for entry in Info.TYPE_CHOICES:
        if user.info.type == entry[0]:
            role = entry[1]

    return role

def auth_course_assignment(user, course):
    pass

class AuthClass:
    pass