from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Officer , Rank


class OfficerForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = Officer
        # fields = "__all__"
        # labels = { "": _("Name of the farmer company"), "FieldName": _("Name of the field") }
        exclude = ("created_by", "updated_by", "created_at", "updated_at")
        
        
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