from TAScheduler.models import Course, Section, User, UserAssignment, Info


class CreateAccountClass:

    def create_user(self, username, email, password, phone, address, type_chosen):
        if User.objects.filter(username=username).exists():
            raise ValueError("User already exists")
        if username == "":
            raise ValueError("Enter required fields.")
        if email == "":
            raise ValueError("Enter required fields.")
        if password == "":
            raise ValueError("Enter required fields.")
        if phone == "":
            raise ValueError("Enter required fields.")
        if address == "":
            raise ValueError("Enter required fields.")
        if type_chosen == "":
            raise ValueError("Enter required fields.")

        new_user = User.objects.create_user(username, email, password)
        new_user.save()

        info = Info(user=new_user, phone=phone, address=address, type=type_chosen)
        info.save()

        return True
