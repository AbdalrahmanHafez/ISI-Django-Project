from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm




class CustomLoginForm(forms.Form):
    username = forms.CharField(label='اسم المستخدم', max_length=254)
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)