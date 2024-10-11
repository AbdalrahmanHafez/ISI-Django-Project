import django_filters
from django import forms
from .models import Officer, Rank, OfficerStatus

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
        widget=forms.CheckboxSelectMultiple,
    )

    is_user_active = django_filters.BooleanFilter(
        field_name='user__is_active',
        widget=forms.CheckboxInput(),
        label="مستخدم غير نشط",
        exclude=True
    )

    no_user = django_filters.BooleanFilter(
        field_name='user',
        lookup_expr='isnull',
        widget=forms.CheckboxInput(),
        label="بدون مستخدم",
    )


    @property
    def qs(self):
        # Get the base queryset and apply the ordering by rank_id
        queryset = super().qs
        return queryset.order_by('rank_id')