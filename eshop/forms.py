from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email', 'password1', 'password2']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'email']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['last_name', 'first_name', 'phone', 'address']