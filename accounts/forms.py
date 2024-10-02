from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm ,PasswordChangeForm,UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User

from officers_affairs.models import Officer

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']
        exclude =  ['password']
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']  # Explicitly remove the password field if present
            
         # Add CSS classes to make the fields smaller and add custom styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm text-center'  # Smaller fields and centered text
            })
            
class OfficerProfileForm(forms.ModelForm):
    class Meta:
        model = Officer
        fields = ['profile_image']  # Include any additional fields you want to allow for editing
     
        
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
