# App_Login\forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # collect email from input
    email = forms.EmailField(label="Email Address", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
