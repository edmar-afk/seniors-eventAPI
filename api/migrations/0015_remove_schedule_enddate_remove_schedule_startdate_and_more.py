# Generated by Django 5.0.6 on 2024-08-11 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_schedule_month_alter_schedule_enddate_and_more'),
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
            name='endDatetime',
            field=models.TimeField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='startDatetime',
            field=models.TimeField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='month',
            field=models.DateField(null=True, blank=True),
            preserve_default=False,
        ),
    ]
