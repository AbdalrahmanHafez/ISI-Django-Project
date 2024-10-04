from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Job, LeaveRequest, Officer, OfficerStatus , Rank, Section, Unit, UnitStatus, Weapon
from django.contrib.auth.models import User,Group


class OfficerForm(LoginRequiredMixin, forms.ModelForm):
    
    create_user = forms.BooleanField(required=False, label="إنشاء مستخدم للضابط")
    
    class Meta:
        model = Officer
        exclude = ("created_by", "updated_by", "created_at", "updated_at","user")
    
    def save(self, commit=True):
        officer = super().save(commit=False)
        
        # Check if we need to create a user
        if self.cleaned_data.get('create_user') and not officer.user:
            username = officer.full_name.lower().replace(" ", "_")

            # Ensure username uniqueness before creating the user
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password='123')
                officer.user = user
                 
                # Assign user to group based on branch
                # if officer.branch:
                #     group, created = Group.objects.get_or_create(name=officer.branch.name)
                #     user.groups.add(group)
                
                
            else:
                self.add_error('create_user', "هناك مستخدم له نفس اسم المستخدم بالفعل !!!")
                
        # Handle updating user group if the branch has changed
        # if officer.user:
        #     if officer.pk:  # Check if officer is being updated
        #         original_officer = Officer.objects.get(pk=officer.pk)
        #         if original_officer.branch != officer.branch:
        #             # Remove user from the old branch group
        #             if original_officer.branch:
        #                 old_group, created = Group.objects.get_or_create(name=original_officer.branch.name)
        #                 officer.user.groups.remove(old_group)

        #             # Add user to the new branch group
        #             if officer.branch:
        #                 new_group, created = Group.objects.get_or_create(name=officer.branch.name)
        #                 officer.user.groups.add(new_group)
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


        if commit:
            officer.save()

        return officer
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        fields = ['leave_type', 'start_date', 'end_date',]
        labels = {
            'leave_type': 'نوع الإجازة',
            'start_date': 'تاريخ البدء',
            'end_date': 'تاريخ الانتهاء',
            
        }
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'hijri-picker form-control', 'placeholder': 'اختر تاريخ البدء'}),
            'end_date': forms.DateInput(attrs={'class': 'hijri-picker form-control', 'placeholder': 'اختر تاريخ الانتهاء'}),
            'days_taken': forms.HiddenInput(),  # حقل مخفي
            'remaining_days': forms.HiddenInput(),  # حقل مخفي
        }
        exclude = ('created_by',)