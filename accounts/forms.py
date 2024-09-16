from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm ,PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField



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
    
    
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="كلمة السر الحالية",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )
    new_password1 = forms.CharField(
        label="كلمة السر الجديدة",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    new_password2 = forms.CharField(
        label="تأكيد كلمة السر الجديدة",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
