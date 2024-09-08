# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

class Rank(models.Model):
    RANK_CHOICES = [
        ('7','ملازم'),
        ('6','ملازم أول' ),
        ('5', 'نقيب'),
        ('4', 'رائد'),
        ('3', 'مقدم'),
        ('2', 'عقيد'),
        ('1', 'عميد'),
    ]
    
    name = models.CharField(max_length=100, choices=RANK_CHOICES , unique=True)
    image = models.ImageField(upload_to='ranks/', null=True, blank=True)  # لحفظ صورة الرتبة

    def __str__(self):
        return self.name

class BloodType(models.Model):
    type = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.type

class Weapon(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




class UnitStatus(models.Model):
 # Define your choices for unit status
    UNIT_STATUS_CHOICES = [
        (1, _('موجود')),   # Available
        (2, _('مأمورية')),   # Mission
        (0, _('منقول')),   # Transferred
    ]

    # Fields for the Officer model
    name = models.CharField(max_length=100)
    unit_status = models.IntegerField(choices=UNIT_STATUS_CHOICES)

    def __str__(self):
        return self.name



class Officer(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="اسم الضابط")
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الرتبة")
    military_number = models.CharField(max_length=50, unique=True, verbose_name="الرقم العسكري")
    seniority_number = models.CharField(max_length=50, verbose_name="رقم الاقدمية")
    national_id = models.CharField(
        max_length=14,
        validators=[MinLengthValidator(14)],
        blank=True,
        null=True,
        verbose_name="الرقم القومي"
    )
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="فصيلة الدم")
    weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="السلاح")
    phone1 = models.CharField(max_length=15, verbose_name="رقم الهاتف 1")
    phone2 = models.CharField(max_length=15, blank=True, null=True, verbose_name= "رقم الهاتف 2")
    home_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم هاتف المنزل")
    marital_status = models.CharField(max_length=50, blank=True, null=True, verbose_name="الحالة الاجتماعية")
    address = models.TextField(verbose_name="العنوان")
    profile_image = models.ImageField(upload_to='officers/', null=True, blank=True, verbose_name="الصورة الشخصية")
    birth_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الميلاد")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_unit', verbose_name="الوحدة")
    join_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الانضمام")
    previous_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_units', verbose_name="الوحدة السابقة")
    status = models.IntegerField(default=1 , choices=[(1, _('خدمة')), (0, _('معاش'))], verbose_name="الحالة")
    unit_status = models.ForeignKey(UnitStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحالة بالوحدة")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفرع")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="القسم")
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الوظيفة")
    batch_number = models.CharField(max_length=5, blank=True, null=True, verbose_name="رقم الدفعة")
    rank_promotion_date = models.DateField(blank=True, null=True, verbose_name="تاريخ آخر ترقي")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_officers')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_officers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
