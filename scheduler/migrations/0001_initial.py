# Generated by Django 4.1.7 on 2023-07-19 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='task-2023_07_19_17_04_26', max_length=200)),
                ('Start_now', models.BooleanField(default=False)),
                ('user', models.CharField(default='admin', max_length=20)),
                ('Schedule_Day', models.CharField(default='mon-sun', max_length=20)),
                ('Schedule_Hour', models.CharField(default='2', max_length=20)),
                ('Schedule_Minute', models.CharField(default='0', max_length=20)),
                ('Username', models.CharField(default='yifenghuang@hotmail.com', max_length=20)),
                ('Password', models.CharField(default='LaoYeGolf', max_length=20)),
                ('Website_Url', models.CharField(default='https://foreupsoftware.com/booking/20945#/login', max_length=50)),
                ('Time_Slot_first_pick', models.TimeField()),
            ],
        ),
    ]
