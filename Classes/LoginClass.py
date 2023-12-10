from django.contrib.auth import authenticate, login

from TAScheduler.models import Course, Section, User, UserAssignment, Info


class LoginClass():

    def validate_login_fields(self, request, username, password):
        if username is None or username == '':
            return 'This field is required'
        if not User.objects.filter(username=username).exists():
            return 'Incorrect username'
        if password is None or password == '':
            return 'This field is required'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return 'Success'
        else:
            return 'Incorrect password'
