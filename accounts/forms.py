from django import forms  # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # type: ignore
from django.contrib.auth.models import User  # type: ignore


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("That email is already in use.")
        return email


class LoginForm(AuthenticationForm):
    pass