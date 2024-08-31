# models.py

from django.db import models
from django.contrib.auth.models import User


class Rank(models.Model):
    
    RANK_CHOICES = [
        ('ملازم','ملازم'),
        ('ملازم أول','ملازم أول' ),
        ('نقيب', 'نقيب'),
        ('رائد', 'رائد'),
        ('مقدم', 'مقدم'),
        ('عقيد', 'عقيد'),
        ('عميد', 'عميد'),
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




class Officer(models.Model):
    full_name = models.CharField(max_length=255)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    military_number = models.CharField(max_length=50, unique=True)
    seniority_number = models.CharField(max_length=50)
    national_id = models.CharField(max_length=14, blank=True, null=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True, blank=True)
    weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True, blank=True)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    home_phone = models.CharField(max_length=15, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='officers/', null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_unit')
    join_date = models.DateField(blank=True, null=True)
    previous_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_units')
    status = models.CharField(max_length=20, choices=[('خدمة', 'خدمة'), ('معاش', 'معاش')])
    unit_status = models.CharField(max_length=50, choices=[('موجود', 'موجود'), ('منقول', 'منقول'), ('مأمورية', 'مأمورية')])
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    batch_number = models.CharField(max_length=5, blank=True, null=True)
    rank_promotion_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_officers')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_officers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
