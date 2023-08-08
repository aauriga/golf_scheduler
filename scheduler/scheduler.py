import random
from datetime import datetime, timedelta
import time

import pytz
from django.utils import timezone
from ntplib import NTPClient
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from threading import Thread

from django.db.models.signals import post_save
from django.dispatch import receiver
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.models import Scheduler

from .views import book_golf, my_job
from .models import Scheduler

urlpatterns = [
]


def apply_offset_to_time(time_field_value, day_value):
    # Dictionary to map day string to integer value
    day_mapping = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}

    # Create an NTP client
    client = NTPClient()

    # Get the current real-world time from a public NTP server
    response = client.request('pool.ntp.org')
    real_world_time = datetime.fromtimestamp(response.tx_time, pytz.timezone('America/Chicago'))

    # Get the current local system time
    local_time = datetime.now(pytz.timezone('America/Chicago'))

    # Calculate the offset between the real-world time and the local system time
    offset = real_world_time - local_time

    # Combine the TimeField value with the current date to create a datetime object
    time_with_offset = datetime.combine(datetime.today().date(), time_field_value)

    # Apply the offset to the given TimeField value
    time_with_offset -= offset

    # Get the corresponding integer value for the given day_value
    day_index = day_mapping.get(day_value.lower())

    # Apply the offset to the day_index to get the modified day_of_week
    modified_day_index = (day_index + time_with_offset.weekday() - local_time.weekday()) % 7
    modified_day_of_week = list(day_mapping.keys())[list(day_mapping.values()).index(modified_day_index)]

    return time_with_offset, modified_day_of_week


scheduler_1 = BackgroundScheduler()
scheduler_1.add_jobstore(DjangoJobStore(), "default")
scheduler_1.add_job(my_job, 'interval', seconds=27, id='something', replace_existing=True)
scheduler_1.start()


def error_handling_book_time(url, username, password, date_time, date, email, date1, date2, bool1, thread, result):
    try:
        book_golf(url, username, password, date_time, date, email, date1, date2, bool1, str(thread))
        return True
    except Exception as e:
        print(str(e))
        return False


def convert_datetime_str(datetime_str: str, in_format='%Y-%m-%d %H:%M:%S%z', out_format='%Y-%m-%d') -> str:
    """
    Convert a datetime string from one format to another.
    :param datetime_str: datetime string in 'in_format' format.
    :param in_format: input datetime string format. Default is '%Y-%m-%d %H:%M:%S%z'.
    :param out_format: output datetime string format. Default is '%Y-%m-%d'.
    :return: datetime string in 'out_format' format.
    """
    # Parse the input datetime string into a datetime object
    dt = datetime.strptime(datetime_str, in_format)

    # Format the datetime object into the output string format
    return dt.strftime(out_format)


def retry_wrapper(target_func, max_retries, id, *args):
    retries = 0
    while retries < max_retries:
        result = target_func(*args)
        if result is True:  # Replace this line with the appropriate success condition for your use case
            break
        retries += 1
        print(f"Retrying function {target_func.__name__} {retries}...  " + str(id))
        time.sleep(random.uniform(1, 2))


@receiver(post_save, sender=Scheduler)
def job_scheduler_start_now(**kwargs):
    task_scheduler_obj = Scheduler.objects.get(user='admin')
    time_field_value = apply_offset_to_time(task_scheduler_obj.Schedule_Time, task_scheduler_obj.Job_1_Schedule_Day)
    print(str(time_field_value[0].strftime('%Y-%m-%d %H:%M:%S')))
    print(str(time_field_value[1]))
    scheduler_1.add_job(job_scheduler_start_period, 'cron', day_of_week=time_field_value[1],
                        hour=time_field_value[0].hour,
                        minute=time_field_value[0].minute,
                        second=time_field_value[0].second+1, id='period_task',
                        replace_existing=True, misfire_grace_time=1000)


def job_scheduler_start_period():
    client = NTPClient()
    scheduler_obj = Scheduler.objects.get(user='admin')
    next_run_job = scheduler_1.get_job('period_task', jobstore='default')
    next_run_date = next_run_job.next_run_time
    scheduled_date = convert_datetime_str(str(next_run_date))
    ntp_time = datetime.fromtimestamp(client.request('pool.ntp.org').tx_time)
    print('Booking job running at Internet timestamp: ' + ntp_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('Booking job running at Local timestamp:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    result = [None] * 5
    threads = [
        Thread(target=retry_wrapper, args=(
            error_handling_book_time, 5, 1, scheduler_obj.Website_Url, scheduler_obj.Username_1,
            scheduler_obj.Password_1,
            scheduler_obj.Time_Slot_1, scheduler_obj.Date_1, scheduler_obj.Email, scheduled_date,
            str(scheduler_obj.Date_1),
            scheduler_obj.Start_1, 1, result)),
        Thread(target=retry_wrapper, args=(
            error_handling_book_time, 5, 2, scheduler_obj.Website_Url, scheduler_obj.Username_1,
            scheduler_obj.Password_1,
            scheduler_obj.Time_Slot_2, scheduler_obj.Date_2, scheduler_obj.Email, scheduled_date,
            str(scheduler_obj.Date_2),
            scheduler_obj.Start_2, 2, result)),
        Thread(target=retry_wrapper, args=(
            error_handling_book_time, 5, 3, scheduler_obj.Website_Url, scheduler_obj.Username_2,
            scheduler_obj.Password_2,
            scheduler_obj.Time_Slot_3, scheduler_obj.Date_3, scheduler_obj.Email, scheduled_date,
            str(scheduler_obj.Date_3),
            scheduler_obj.Start_3, 3, result)),
        Thread(target=retry_wrapper, args=(
            error_handling_book_time, 5, 4, scheduler_obj.Website_Url, scheduler_obj.Username_2,
            scheduler_obj.Password_2,
            scheduler_obj.Time_Slot_4, scheduler_obj.Date_4, scheduler_obj.Email, scheduled_date,
            str(scheduler_obj.Date_4),
            scheduler_obj.Start_4, 4, result))
    ]
    for thread in threads:
        thread.start()
        time.sleep(1.5)

    for thread in threads:
        thread.join()
