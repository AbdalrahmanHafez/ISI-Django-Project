# Generated by Django 5.0.8 on 2024-09-29 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0003_alter_officer_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='remaining_days',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
