# Generated by Django 5.0.8 on 2024-09-28 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0002_leaverequest_days_taken_alter_leaverequest_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='role',
            field=models.CharField(blank=True, choices=[('المدير', 'المدير'), ('رئيس فرع شئون ضباط', 'رئيس فرع شئون ضباط'), ('نائب المدير', 'نائب المدير'), ('رئيس فرع السكرتارية', 'رئيس فرع السكرتارية')], max_length=50, null=True, verbose_name='الوظيفة'),
        ),
    ]
