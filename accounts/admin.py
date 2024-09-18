from django.contrib import admin
from officers_affairs.models import Officer
from officers_affairs.forms import OfficerForm

class OfficerAdmin(admin.ModelAdmin):
    form = OfficerForm
    list_display = ['full_name', 'rank', 'birth_date', 'user']

    def save_model(self, request, obj, form, change):
        # Automatically create user when officer is created
        super().save_model(request, obj, form, change)