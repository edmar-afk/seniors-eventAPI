# Generated by Django 5.0.6 on 2024-08-10 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_schedule_notification_pension'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='endDate',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='startDate',
        ),
        migrations.AddField(
            model_name='schedule',
            name='end_time',
            field=models.TimeField(default="14:30:00"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='start_time',
            field=models.TimeField(default="14:30:00"),
            preserve_default=False,
        ),
    ]
