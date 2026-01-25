from django.urls import path  # type: ignore
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.JMLoginView.as_view(), name="login"),
    path("logout/", views.JMLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]