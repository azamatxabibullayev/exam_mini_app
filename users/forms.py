from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=200, required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email']
