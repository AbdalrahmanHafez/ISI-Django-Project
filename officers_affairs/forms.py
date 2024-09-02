from django import forms
from .models import Officer


class OfficerForm(forms.ModelForm):
    class Meta:
        model = Officer
        fields = "__all__"