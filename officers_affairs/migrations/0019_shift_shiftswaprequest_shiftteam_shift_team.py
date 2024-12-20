# Generated by Django 5.0.8 on 2024-10-12 00:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officers_affairs', '0018_alter_leaverequest_compensation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_holiday', models.BooleanField(default=False)),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='officers_affairs.officer')),
            ],
        ),
        migrations.CreateModel(
            name='ShiftSwapRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('new_shift', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_shift', to='officers_affairs.shift')),
                ('original_shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original_shift', to='officers_affairs.shift')),
                ('requesting_officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swap_requests', to='officers_affairs.officer')),
                ('target_officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swap_targets', to='officers_affairs.officer')),
            ],
        ),
        migrations.CreateModel(
            name='ShiftTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_type', models.CharField(choices=[('قائد منوب', 'قائد منوب'), ('ضابط نوبطچي', 'ضابط نوبطچي')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('officer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shift_teams', to='officers_affairs.officer')),
            ],
        ),
        migrations.AddField(
            model_name='shift',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='officers_affairs.shiftteam'),
        ),
    ]
