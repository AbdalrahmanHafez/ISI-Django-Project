from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from django import forms
from . import views
from . import forms




urlpatterns = [
    path('login/', auth_views.LoginView.as_view(next_page= reverse_lazy("home"),template_name= 'accounts/login.html', authentication_form= forms.CustomAuthenticationForm, redirect_authenticated_user= True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/login"), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('profile/', views.profile_view, name='profile_view'),
]
