from django.contrib import messages  # type: ignore
from django.contrib.auth import login  # type: ignore
from django.contrib.auth.views import LoginView, LogoutView  # type: ignore
from django.shortcuts import redirect, render  # type: ignore

from .forms import RegisterForm, LoginForm


class JMLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("orders:order_list")
        return super().dispatch(request, *args, **kwargs)


class JMLogoutView(LogoutView):
    # LOGOUT_REDIRECT_URL is already set in settings.py, so we can keep it simple
    pass


def register(request):
    if request.user.is_authenticated:
        return redirect("orders:order_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You’re now logged in.")
            return redirect("orders:order_list")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
