from datetime import timedelta, datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# Create your models here.
def one_week_ahead():
    return timezone.now() + timedelta(weeks=1)


class Scheduler(models.Model):

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
    user = models.CharField(max_length=20, default='admin')
    Schedule_Time = models.TimeField(null=True, blank=True)
    Job_1_Pre_Start_Time = models.TimeField(null=True, blank=True)
    Job_1_Schedule_Day = models.CharField(max_length=20, default='sun')
    Username_1 = models.CharField(max_length=30, default='yifenghuang@hotmail.com')
    Password_1 = models.CharField(max_length=20, default='LaoYeGolf')
    Username_2 = models.CharField(max_length=30, default='husgarden1@gmail.com')
    Password_2 = models.CharField(max_length=20, default='garden2227')
    Website_Url = models.CharField(max_length=50, default='https://foreupsoftware.com/booking/20954#/login')
    Email = models.CharField(max_length=50, default='zhen.gong@predictifsolutions.com')
    Number_of_Retries = models.IntegerField(default=3)
    Wait_Between_Thread = models.FloatField(default=0.5)
    Start_1 = models.BooleanField(default=False)
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
    Start_5 = models.BooleanField(default=False)
    Date_5 = models.DateField(default=one_week_ahead)
    Time_Slot_5 = models.TimeField(default=datetime.now)
    Time_Slot_6 = models.TimeField(default=datetime.now)
    Start_6 = models.BooleanField(default=False)
    Date_6 = models.DateField(default=one_week_ahead)
    Time_Slot_6 = models.TimeField(default=datetime.now)

    def __str__(self):
        return self.title
