from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm ,PasswordChangeForm,UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

from officers_affairs.models import Officer

class ArabicFileInput(ClearableFileInput):
    template_name = ''  # We'll render directly in the `render` method

    def render(self, name, value, attrs=None, renderer=None):
        # Customize the input field HTML with Arabic labels
        html = f'''
            <style>
              .custom-file-input {{
                display: none;  /* Hide the default file input */
              }}
              .custom-file-label {{
                display: inline-block;
                padding: 0.2em 0.7em;
                border: 1px solid #ccc;
                cursor: pointer;
              }}
              .file-name {{
                margin-right: 10px;
                color: #666;
              }}
            </style>
            
            <div class="form-group">
                <label class="custom-file-label" for="{attrs['id']}">اختر ملف</label>
                <input type="file" class="custom-file-input" id="{attrs['id']}" name="{name}">
                <span class="file-name">{'لم يتم اختيار ملف' if not value else 'حالياً: ' + str(value)}</span>
        '''

        # If a file exists (i.e., if value is provided), add the clear checkbox near the label
        if value:
            clear_checkbox_name = self.clear_checkbox_name(name)
            clear_checkbox_id = self.clear_checkbox_id(clear_checkbox_name)
            clear_label = 'إزالة الصورة الحالية'  # Clear image in Arabic

            html += f'''
                <span style="margin-left: 20px;">
                    <input type="checkbox" class="form-check-input" id="{clear_checkbox_id}" name="{clear_checkbox_name}">
                    <label class="form-check-label" for="{clear_checkbox_id}">{clear_label}</label>
                </span>
            '''

        # Close the form-group div
        html += '</div>'

        # Add a script to handle file input change
        html += f'''
            <script>
              const fileInput = document.getElementById('{attrs['id']}');
              const fileNameDisplay = document.querySelector('.file-name');
              
              fileInput.addEventListener('change', function () {{
                const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : 'لم يتم اختيار ملف';
                fileNameDisplay.textContent = fileName;
              }});
            </script>
        '''

        return mark_safe(html)


class ArabicClearableFileInput(ClearableFileInput):
    initial_text = "الصورة الحالية"
    input_text = "تغيير"
    clear_checkbox_label = "مسح الصورة"

    template_name = 'widgets/arabic_clearable_file_input.html'

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']
        exclude =  ['password']
        error_messages = {
            'username': {
                'unique': "اسم المستخدم هذا موجود بالفعل.", 
                'required': "يرجى إدخال اسم المستخدم.",
                'max_length': "اسم المستخدم يجب أن يكون أقل من 150 حرفًا.",
            }
        }
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "اسم المستخدم"
        self.fields['username'].help_text = ""


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
        fields = ['profile_image'] 


    def __init__(self, *args, **kwargs):
        super(OfficerProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['profile_image'].widget.clear_checkbox_label = "مسح الصورة"
        # self.fields['profile_image'].widget = ArabicClearableFileInput()
        self.fields['profile_image'].widget = ArabicFileInput()

     
        
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
