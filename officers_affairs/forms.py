from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  Job, LeaveRequest, Officer, OfficerStatus , Rank, Section, Unit, UnitStatus, Weapon
from django.contrib.auth.models import User,Group


class OfficerForm(LoginRequiredMixin, forms.ModelForm):
    create_user = forms.BooleanField(initial=True, required=False, label="إنشاء مستخدم للضابط")
    is_active = forms.BooleanField(initial=True, required=False, label="المستخدم نشط")

    class Meta:
        model = Officer
        exclude = ("created_by", "updated_by", "created_at", "updated_at","user")


    def clean(self):
        cleaned_data = super().clean()
        create_user = cleaned_data.get('create_user')
        full_name = cleaned_data.get('full_name')

        if create_user:
            username = full_name.lower().replace(" ", "_")

            if User.objects.filter(username=username).exists():
                self.add_error('full_name', "هناك مستخدم له نفس اسم المستخدم بالفعل ")
        
        return cleaned_data
    
    def save(self, commit=True):
        officer = super().save(commit=False)
        
        # Check if we need to create a user
        if self.cleaned_data.get('create_user') and not officer.user:
            username = officer.full_name.lower().replace(" ", "_")
            user = User.objects.create_user(username=username, password='123')
            officer.user = user
                 

        # Handle updating user branch if the branch has changed
        if officer.user:
            if officer.pk:  # Check if officer is being updated
                original_officer = Officer.objects.get(pk=officer.pk)
                
                # If the user's branch has changed
                if original_officer.branch != officer.branch:
                    # Remove user from the old branch
                    if original_officer.branch:
                        officer.user.groups.remove(original_officer.branch)

                    # Add user to the new branch
                    if officer.branch:
                        new_branch = officer.branch
                        officer.user.groups.clear()  # Clear any existing groups to ensure only one branch
                        officer.user.groups.add(new_branch)

            else:
                # If the officer is being created, assign the branch directly
                if officer.branch:
                    new_branch = officer.branch
                    officer.user.groups.clear()  # Clear any existing groups to ensure only one branch
                    officer.user.groups.add(new_branch)

            officer.user.is_active = self.cleaned_data.get('is_active', True) 
            officer.user.save()


        if commit:
            officer.save()

        return officer
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk != None: # Update Officer
            if self.instance.user:
                self.fields['is_active'].initial = self.instance.user.is_active  
                del self.fields['create_user']
            else:
                self.fields['create_user'].initial = False
        



        for field_name, field in self.fields.items():
                    if isinstance(field, forms.DateField):
                        field.widget.attrs.update({
                            'class': 'hijri-picker form-control',  
                            'type': 'text',  
            })
             

class WeaponForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            
        }
        
class BranchForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            
        }
        
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'branch']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'branch': forms.Select(attrs={'class':'form-control'})
            
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name','section']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'section': forms.Select(attrs={'class':'form-control'})
            
        }        
        
class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            
        }
        
        
        
class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ['name','image']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }



class OffUnitStatusForm(forms.ModelForm):
    class Meta:
        model = UnitStatus
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
        }        
        
        
class OfficerStatusForm(forms.ModelForm):
    class Meta:
        model = OfficerStatus
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
        }
        
        
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'compensation_date']
        labels = {
            'leave_type': 'نوع الإجازة',
            'start_date': 'تاريخ البدء',
            'end_date': 'تاريخ الانتهاء',
            'compensation_date': "بدل عن يوم",
        }
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'hijri-picker form-control', 'placeholder': 'اختر تاريخ البدء'}),
            'end_date': forms.DateInput(attrs={'class': 'hijri-picker form-control', 'placeholder': 'اختر تاريخ الانتهاء'}),
            'days_taken': forms.HiddenInput(),  # حقل مخفي
            'remaining_days': forms.HiddenInput(),
            'compensation_date': forms.DateInput(attrs={'class': 'hijri-picker form-control', 'placeholder': 'اختر تاريخ'}),
        }
        exclude = ('created_by',)
        
    def clean(self):
        cleaned_data = super().clean()
        leave_type = cleaned_data.get('leave_type')
        compensation_date = cleaned_data.get('compensation_date')

        # Check if leave_type is 'instead_of_rest' and compensation_date is not provided
        if leave_type == LeaveRequest.INSTEAD_OF_REST and not compensation_date:
            self.add_error('compensation_date', 'تاريخ البدل مطلوب لنوع اجازة بدل راحة')

        return cleaned_data

    # if in model
    # def clean(self):
    #     super().clean()
        
    #     # Check if leave_type is 'instead_of_rest' and compensation_date is not provided
    #     if self.leave_type == self.INSTEAD_OF_REST and not self.compensation_date:
    #         raise ValidationError({
    #             'compensation_date': 'تاريخ البدل مطلوب لنوع اجازة بدل راحة'
    #         })
        
        
        
        
# class DailyAttendanceForm(forms.ModelForm):
#     class Meta:
#         model = DailyAttendance
#         fields = ['officer', 'date', 'status', 'leave_type', 'mission_details']
#         widgets = {
#             'date': forms.DateInput(attrs={'class': 'hijri-picker', 'placeholder': 'تاريخ'}),
#             'mission_details': forms.Textarea(attrs={'rows': 2}),
#         }
#         labels = {
#             'officer': 'الضابط',
#             'date': 'تاريخ',
#             'status': 'الحالة',
#             'leave_type': 'نوع الإجازة',
#             'mission_details': 'تفاصيل المأمورية',
#         }