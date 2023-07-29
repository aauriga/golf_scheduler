from datetime import timedelta, datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# Create your models here.
class Scheduler(models.Model):
    def one_week_ahead():
        return timezone.now() + timedelta(weeks=1)

    def validate_date(value):
        if value < timezone.now().date() or value > (timezone.now().date() + timedelta(days=6)):
            raise ValidationError("Date should be within the next 6 days.")

    NUMBER_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    ]

    title = models.CharField(
        max_length=200,
        default='task-' + str(timezone.now().strftime('%Y_%m_%d_%H_%M_%S')))
    Start_now = models.BooleanField(default=False)
    user = models.CharField(max_length=20, default='admin')
    Job_1_Schedule_Day = models.CharField(max_length=20, default='sun')
    Job_1_Schedule_Hour = models.CharField(max_length=20, default='2')
    Job_1_Schedule_Minute = models.CharField(max_length=20, default='0')
    Username_1 = models.CharField(max_length=30, default='yifenghuang@hotmail.com')
    Password_1 = models.CharField(max_length=20, default='LaoYeGolf')
    Username_2 = models.CharField(max_length=30, default='husgarden1@gmail.com')
    Password_2 = models.CharField(max_length=20, default='garden2227')
    Website_Url = models.CharField(max_length=50, default='https://foreupsoftware.com/booking/20954#/login')
    Email = models.CharField(max_length=50, default='zhen.gong@predictifsolutions.com')
    Date_1 = models.DateField(default=one_week_ahead)
    Time_Slot_1 = models.TimeField(default=datetime.now)
    Start_2 = models.BooleanField(default=False)
    Date_2 = models.DateField(default=one_week_ahead)
    Time_Slot_2 = models.TimeField(default=datetime.now)
    Start_3 = models.BooleanField(default=False)
    Date_3 = models.DateField(default=one_week_ahead)
    Time_Slot_3 = models.TimeField(default=datetime.now)
    Start_4 = models.BooleanField(default=False)
    Date_4 = models.DateField(default=one_week_ahead)
    Time_Slot_4 = models.TimeField(default=datetime.now)
    def __str__(self):
        return self.title
