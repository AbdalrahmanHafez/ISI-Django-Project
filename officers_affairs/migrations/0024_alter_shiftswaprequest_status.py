# Generated by Django 5.0.8 on 2024-10-19 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0023_remove_shiftswaprequest_is_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftswaprequest',
            name='status',
            field=models.CharField(choices=[('pending', 'جـاري التصديــق'), ('approved', 'تصــدق'), ('rejected', 'لم يتصدق')], default='pending', max_length=200, verbose_name='الحالة'),
        ),
    ]