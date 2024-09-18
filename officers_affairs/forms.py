from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Officer , Rank
from django.contrib.auth.models import User


class OfficerForm(LoginRequiredMixin, forms.ModelForm):
    
    create_user = forms.BooleanField(required=False, label="Create corresponding user")
    
    class Meta:
        model = Officer
        # fields = "__all__"
        # labels = { "": _("Name of the farmer company"), "FieldName": _("Name of the field") }
        exclude = ("created_by", "updated_by", "created_at", "updated_at", "user")
    
    def save(self, commit=True):
        officer = super().save(commit=False)

        if not officer.user:
            # Create a User instance
            username = officer.full_name.lower().replace(" ", "_")
            user = User.objects.create_user(username=username, password='123')  # Default passworduser = User.objects.create(username=username)
            officer.user = user

      

        return officer    
        
        
        # widgets = {
        #     'birth_date': forms.DateInput(
        #         attrs={
        #             'class': 'form-control', 
        #             'id': 'hijri-picker', 
        #             'placeholder': 'DD-MM-YYYY'
        #         },
        #         format='%d-%m-%Y'  # Match your desired format
        #     ),
        #     }
       
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Set the input format for birth_date to match the widget
    #     self.fields['birth_date'].input_formats = ['%d-%m-%Y']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.DateField):
                field.widget.attrs.update({
                    'class': 'hijri-picker form-control',  
                    'type': 'text',  
                })
             

class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ['name','image']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }