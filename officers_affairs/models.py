# models.py
from django.db import models
from django.contrib.auth.models import User,Group
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone





class Rank(models.Model):
    
    name = models.CharField(max_length=100, unique=True,verbose_name="الرتبه")
    image = models.ImageField(upload_to='ranks/', null=True, blank=True,verbose_name="")
    def __str__(self):
        return self.name

class BloodType(models.Model):
    type = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.type

class Weapon(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name="الســلاح")

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name="الــوحدة")

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name="الـقسم")
    branch = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='sections',verbose_name="الـفرع")
    def __str__(self):
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=100, unique=True,verbose_name="الوظيفه")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name='jobs',verbose_name="القسم")
    def __str__(self):
        return self.name




class UnitStatus(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=" حالة الضابط بالوحدة")

    def __str__(self):
        return self.name
    
    
class MaritalStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class OfficerStatus(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="حالة الضابط")

    def __str__(self):
        return self.name



class Officer(models.Model):
    
    ROLE_CHOICES = [
        ('المدير', 'المدير'),
        ('رئيس فرع شئون ضباط', 'رئيس فرع شئون ضباط'),
        ('نائب المدير', 'نائب المدير'),
        ('رئيس فرع السكرتارية', 'رئيس فرع السكرتارية'),
    ]
    
    is_leader = models.BooleanField(default=False, verbose_name="قائد الفرع")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True, blank=True, verbose_name="الوظيفة الادارية")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile', null=True,blank=True)
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
    phone1 = models.CharField(max_length=15, verbose_name="رقم الهاتف ١")
    phone2 = models.CharField(max_length=15, blank=True, null=True, verbose_name= "رقم الهاتف ٢")
    home_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="رقم هاتف المنزل")
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحالة الإجتماعية")
    address = models.CharField(max_length=255,verbose_name="العنوان")
    profile_image = models.ImageField(upload_to='officers/', null=True, blank=True, verbose_name="الصورة الشخصية")
    birth_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الميلاد")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_unit', verbose_name="الوحدة")
    join_date = models.DateField(blank=True, null=True, verbose_name="تاريخ الانضمام")
    previous_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_units', verbose_name="الوحدة السابقة")
    status = models.ForeignKey(OfficerStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحالة")
    unit_status = models.ForeignKey(UnitStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحالة بالوحدة")
    branch = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الفرع")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="القسم")
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الوظيفه")
    batch_number = models.CharField(max_length=40, blank=True, null=True, verbose_name="رقم الدفعة")
    rank_promotion_date = models.DateField(blank=True, null=True, verbose_name="تاريخ آخر ترقي")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_officers')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_officers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
    
#جدول طلبات الأجازة

class LeaveRequest(models.Model):
    ANNUAL_LEAVE = 'annual'
    CASUAL_LEAVE = 'casual'
    LEADER_GRANT = 'leader_grant'
    INSTEAD_OF_REST = 'instead_of_rest'
    REST = 'rest'
    
    LEAVE_TYPES = [
        (ANNUAL_LEAVE, "سنوية"),
        (CASUAL_LEAVE, "عارضة"),
        (LEADER_GRANT, "منحة قائد"),
        (INSTEAD_OF_REST, "بدل راحة"),
        (REST, " راحة"),
    ]
    
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'جـاري التصديــق'),
        (APPROVED, 'تصــدق'),
        (REJECTED, 'لم يتصدق'),
    ]
    
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='leave_requests', verbose_name="الضابط")
    approver = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="المصدق الحالي")
    final_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='final_approver', verbose_name="المصدق النهائي")
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES, verbose_name="نوع الإجازة")
    start_date = models.DateField(verbose_name="تاريخ بداية الإجازة")
    end_date = models.DateField(verbose_name="تاريخ انتهاء الإجازة")
    reason = models.TextField(blank=True, verbose_name="السبب")
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=PENDING, verbose_name="الحالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_leave_request')
    days_taken = models.PositiveIntegerField(default=0, verbose_name="عدد الأيام المأخوذة")
    remaining_days = models.IntegerField(null=True, blank=True ,  verbose_name="عدد الأيام المتبقية")  # الأيام المتبقية
    compensation_date = models.DateField(null=True, blank=True, verbose_name="بدل عن ترايخ")


    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.days_taken = (self.end_date - self.start_date).days + 1  # +1 لحساب اليوم الأول
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.officer.user.username} - {self.get_leave_type_display()}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)  # Add a link field for redirection

    def __str__(self):
        return self.message
    
    
class DailyAttendance(models.Model):
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, verbose_name="الضابط")
    date = models.DateField(default=timezone.now, verbose_name="التاريخ")
    status = models.ForeignKey(UnitStatus, on_delete=models.SET_NULL, null=True, verbose_name="الحالة اليومية")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    class Meta:
        unique_together = ('officer', 'date')
        verbose_name = 'تمام يومي'
        verbose_name_plural = 'تمامات يومية'

    def __str__(self):
        return f"{self.officer.full_name} - {self.date} - {self.status.name}"  
    
# نوبطجيات 


class ShiftTeam(models.Model):
    TEAM_TYPE_CHOICES = [
        ('قائد منوب', 'قائد منوب'),
        ('ضابط نوبطچي', 'ضابط نوبطچي')
    ]
    team_type = models.CharField(max_length=20, choices=TEAM_TYPE_CHOICES, verbose_name="نوع الطاقم")
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='shift_teams', verbose_name="الضابط")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاريخ الإنشاء")


class Shift(models.Model):
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    team = models.ForeignKey(ShiftTeam, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_holiday = models.BooleanField(default=False)


class ShiftSwapRequest(models.Model):
    requesting_officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='swap_requests', verbose_name="الضابط المقدم للطلب")
    target_officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='swap_targets', verbose_name="الضابط المستهدف")
    original_shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='original_shift', verbose_name="النوبطچية الأصلية")
    new_shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='new_shift', null=True, blank=True, verbose_name="النوبطچية الجديدة")
    is_approved = models.BooleanField(default=False, verbose_name="تمت الموافقة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
