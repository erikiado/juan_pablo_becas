from django import forms

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput())
