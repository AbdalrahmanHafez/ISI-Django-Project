from .models import Officer, Rank
from django import forms
import django_filters
from django.urls import reverse_lazy

    

# class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
#     template_name = "test.html"

class OfficerFilter(django_filters.FilterSet):
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
    
    # rank = django_filters.ModelMultipleChoiceFilter(
    #     field_name='rank',
    #     queryset=Rank.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    # )


    class Meta:
        model = Officer
        # fields = {"full_name": ['icontains']}
        # fields = ["rank"]
        fields = {}


