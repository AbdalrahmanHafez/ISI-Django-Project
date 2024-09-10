from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from . import views

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label= "اسم المستخدم",
        widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label="كلمة السر",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


    error_messages = {
        "invalid_login": "اسم المستخدم او كلمة المرور غير صحيحة",
        "inactive": "This account is inactive.",
    }


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(next_page= reverse_lazy("home"),template_name= 'accounts/login.html', authentication_form= CustomAuthenticationForm, redirect_authenticated_user= True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/login"), name='logout'),
]
