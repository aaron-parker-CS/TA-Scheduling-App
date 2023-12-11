from Classes.AuthClass import auth_type
from TAScheduler.models import Course, Section, User, UserAssignment, Info


class DeleteAccountClass:
    @staticmethod
    def delete_user(user_id):
        try:
            user_to_delete = User.objects.get(id=user_id)
            username = user_to_delete.username
            user_to_delete.delete()
            return f"Account '{username}' deleted successfully.", None
        except User.DoesNotExist:
            return None, "User not found."
