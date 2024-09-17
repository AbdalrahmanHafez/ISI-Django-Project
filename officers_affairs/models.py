# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class Rank(models.Model):
    
    name = models.CharField(max_length=100, unique=True,verbose_name="الرتبه")
    image = models.ImageField(upload_to='ranks/', null=True, blank=True,verbose_name="صورة الرتبه")
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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='sections')
    def __str__(self):
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=100, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name='jobs')
    def __str__(self):
        return self.name




class UnitStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
class MaritalStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class OfficerStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

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
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحالة الاجتماعية")
    address = models.CharField(max_length=255,verbose_name="العنوان")
    profile_image = models.ImageField(upload_to='officers/', null=True, blank=True, verbose_name="الصورة الشخصية")
    birth_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الميلاد")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_unit', verbose_name="الوحدة")
    join_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الانضمام")
    previous_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_units', verbose_name="الوحدة السابقة")
    status = models.ForeignKey(OfficerStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحالة")
    unit_status = models.ForeignKey(UnitStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحالة بالوحدة")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفرع")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="القسم")
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الوظيفة")
    batch_number = models.CharField(max_length=40, blank=True, null=True, verbose_name="رقم الدفعة")
    rank_promotion_date = models.DateField(blank=True, null=True, verbose_name="تاريخ آخر ترقي")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_officers')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_officers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
