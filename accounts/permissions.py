from django.contrib.auth.mixins import UserPassesTestMixin


WRITE_ROLES = {"admin", "analyst", "consultant"}
ADMIN_ROLES = {"admin"}


def user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return "admin"
    return getattr(getattr(user, "profile", None), "role", None)


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = WRITE_ROLES

    def test_func(self):
        return user_role(self.request.user) in self.allowed_roles
