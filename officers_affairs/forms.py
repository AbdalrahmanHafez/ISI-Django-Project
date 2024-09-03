from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Officer

class OfficerForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = Officer
        # fields = "__all__"
        # labels = { "": _("Name of the farmer company"), "FieldName": _("Name of the field") }
        exclude = ("created_by", "updated_by", "created_at", "updated_at")
