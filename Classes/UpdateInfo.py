from TAScheduler.models import User, Info


def updateInfo(user, fname, lname, phone, skills, message=''):
    if user is None:
        message = 'User may not be empty'
        return False

    if fname is None or not fname:
        message = 'First name may not be empty'
        return False
    if lname is None or not fname:
        message = 'Last name may not be empty'
        return False
    if phone is None or not fname:
        message = 'Phone may not be empty'
        return False

    user.first_name = fname
    user.last_name = lname
    user.info.phone = phone
    user.info.skills = skills

    try:
        user.save()
        user.info.save()
        return True
    except Exception as e:
        message = e
        return False
