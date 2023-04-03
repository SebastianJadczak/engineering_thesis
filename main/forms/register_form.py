from django import forms
from django.contrib.auth.models import User


class RegisterFormNewUser(forms.ModelForm):
    username = forms.CharField(label="Login:",
                               max_length=20,
                               widget=forms.TextInput(attrs={'id': 'username_register', }))
    email = forms.EmailField(label="Email:",
                             widget=forms.TextInput(attrs={'id': 'email_register'}))
    password = forms.CharField(label='Hasło:',
                               widget=forms.PasswordInput(attrs={'id': 'password_register'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
