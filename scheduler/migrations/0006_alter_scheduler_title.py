# Generated by Django 4.1.7 on 2023-07-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_scheduler_date_alter_scheduler_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler',
            name='title',
            field=models.CharField(default='task-2023_07_19_17_36_26', max_length=200),
        ),
    ]