# Generated by Django 5.0.8 on 2024-10-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0006_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]