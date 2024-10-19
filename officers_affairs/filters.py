import django_filters
from django import forms
from .models import Officer, Rank, OfficerStatus
import re

def extract_numeric(s):
    # Extract the numeric part of the string using regular expressions
    numbers = re.findall(r'\d+', s)
    return int(numbers[0]) if numbers else float('inf')  # Return infinity if no number is found

class OfficerFilter(django_filters.FilterSet):
    class Meta:
        model = Officer
        fields = {}

    full_name = django_filters.CharFilter(
        field_name='full_name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': '...'}),
        label="اسم الضابط"
    )

    military_number = django_filters.CharFilter(
        field_name='military_number',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': '...'}),
        label="الرقم العسكري"
    )

    seniority_number = django_filters.CharFilter(
        field_name='seniority_number',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': '...'}),
        label="رقم الاقدمية"
    )

    national_id = django_filters.CharFilter(
        field_name='national_id',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': '...'}),
        label="الرقم القومي"
    )

    rank = django_filters.ModelChoiceFilter(
        field_name='rank',
        queryset=Rank.objects.all(),
        widget=forms.Select,  
    )

    status = django_filters.ModelMultipleChoiceFilter(
        field_name='status',
        queryset=OfficerStatus.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'pe-5'}),
    )

    is_user_active = django_filters.BooleanFilter(
        field_name='user__is_active',
        # widget=forms.CheckboxInput(),
        label="مستخدم نشط",
        # exclude=True
        widget= forms.Select(choices=[ ('', 'غير محدد'), (True, 'نعم'), (False, 'لا') ])
    )

    no_user = django_filters.BooleanFilter(
        field_name='user',
        lookup_expr='isnull',
        # widget=forms.CheckboxInput(),
        label="بدون مستخدم",
        widget= forms.Select(choices=[ ('', 'غير محدد'), (True, 'نعم'), (False, 'لا') ])
    )


    @property
    def qs(self):
        # Get the base queryset and apply the ordering by rank_id
        queryset = super().qs

        queryset = sorted(queryset, key=lambda x: extract_numeric(x.seniority_number))
        # return queryset.order_by('rank_id')
        return queryset