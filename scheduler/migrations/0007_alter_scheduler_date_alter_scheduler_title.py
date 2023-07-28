# Generated by Django 4.1.7 on 2023-07-19 17:48

from django.db import migrations, models
import scheduler.models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_alter_scheduler_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler',
            name='Date',
            field=models.DateField(default=scheduler.models.Scheduler.one_week_ahead, validators=[scheduler.models.Scheduler.validate_date]),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='title',
            field=models.CharField(default='task-2023_07_19_17_48_58', max_length=200),
        ),
    ]
