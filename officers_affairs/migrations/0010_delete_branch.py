# Generated by Django 5.0.8 on 2024-10-04 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0009_alter_section_branch'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Branch',
        ),
    ]