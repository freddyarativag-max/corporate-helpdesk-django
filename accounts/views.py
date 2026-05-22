from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView


class StyledLoginView(LoginView):
    template_name = "accounts/login.html"


class StyledLogoutView(LogoutView):
    pass
