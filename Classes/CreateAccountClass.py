from TAScheduler.models import Course, Section, User, UserAssignment, Info


class CreateAccountClass:

    def create_user(self, username, password, firstname, lastname, phone, type_chosen):
        if User.objects.filter(username=username).exists():
            raise ValueError("User already exists")
        if username == "":
            raise ValueError("Enter required fields.")
        if password == "":
            raise ValueError("Enter required fields.")
        if phone == "":
            raise ValueError("Enter required fields.")
        if firstname == "":
            raise ValueError("Enter required fields.")
        if lastname == "":
            raise ValueError("Enter required fields.")
        if type_chosen == "":
            raise ValueError("Enter required fields.")

        new_user = User.objects.create_user(username, str(username)+'@uwm.edu', password)
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.save()

        info = Info(user=new_user, phone=phone, type=type_chosen)
        info.save()

        return True
