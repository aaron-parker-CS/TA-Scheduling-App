from TAScheduler.models import User, Info


def updateInfo(user, fname, lname, phone, message=''):
    if user is None:
        message = 'User may not be empty'
        return message
    if fname is None or not fname:
        message = 'First name may not be empty'
        return message
    if lname is None or not lname:
        message = 'Last name may not be empty'
        return message
    if phone is None or not phone:
        message = 'Phone may not be empty'
        return message

    user.first_name = fname
    user.last_name = lname
    user.info.phone = phone

    try:
        user.save()
        user.info.save()
        return 'True'
    except Exception as e:
        message = e
        return message
