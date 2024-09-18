# Generated by Django 5.0.8 on 2024-09-18 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0005_alter_officer_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='officer_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rank',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ranks/', verbose_name='صورة'),
        ),
    ]
