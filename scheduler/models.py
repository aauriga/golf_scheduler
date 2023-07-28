from datetime import timedelta

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
    Job_2_Start = models.BooleanField(default=False)
    Job_2_Schedule_Day = models.CharField(max_length=20, default='sun')
    Job_2_Schedule_Hour = models.CharField(max_length=20, default='2')
    Job_2_Schedule_Minute = models.CharField(max_length=20, default='0')
    Username = models.CharField(max_length=30, default='yifenghuang@hotmail.com')
    Password = models.CharField(max_length=20, default='LaoYeGolf')
    Website_Url = models.CharField(max_length=50, default='https://foreupsoftware.com/booking/20954#/login')
    Email = models.CharField(max_length=50, default='zhen.gong@predictifsolutions.com')
    Date = models.DateField(default=one_week_ahead, validators=[validate_date])
    Time_Slot = models.TimeField()
    def __str__(self):
        return self.title
