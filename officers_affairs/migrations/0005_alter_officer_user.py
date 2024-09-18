# Generated by Django 5.0.8 on 2024-09-18 02:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0004_alter_officer_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='officer_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
