from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Officer , Rank


class OfficerForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = Officer
        # fields = "__all__"
        # labels = { "": _("Name of the farmer company"), "FieldName": _("Name of the field") }
        exclude = ("created_by", "updated_by", "created_at", "updated_at")
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
        
        
             

class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ['name','image']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }