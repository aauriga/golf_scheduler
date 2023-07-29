from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from .views import book_golf
from .models import Scheduler

urlpatterns = [
]

scheduler_1 = BackgroundScheduler()
scheduler_1.add_jobstore(DjangoJobStore(), "default")


def verify_dates(date1: str, date2: str, date_format='%Y-%m-%d') -> bool:
    """
    Verify if date1 is no longer than 6 days ahead of date2.
    :param date1: date string in 'date_format' format.
    :param date2: date string in 'date_format' format.
    :param date_format: date format string. Default is '%Y-%m-%d' (ISO 8601 date format).
    :return: True if date1 is no longer than 6 days ahead of date2, False otherwise.
    """
    # Parse the date strings into datetime objects
    dt1 = datetime.strptime(date1, date_format) - timedelta(weeks=1)
    dt2 = datetime.strptime(date2, date_format)
    print(dt1, dt2)

    # Calculate the difference in days between the two dates
    diff = (dt2 - dt1).days
    print(diff)

    # Return whether the difference is less than or equal to 6
    return diff <= 6


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



def job_scheduler_start_now():
    task_scheduler_obj = Scheduler.objects.get(user='admin')
    scheduled_time = str(scheduler_1.get_job('period_task').next_run_time)
    # if scheduled_time[11:13] != get_schedule_hour(task_scheduler_obj) or scheduled_time[14:16] != get_schedule_minute(
    #         task_scheduler_obj):
    scheduler_1.add_job(job_scheduler_start_period, 'cron', day_of_week=task_scheduler_obj.Job_1_Schedule_Day,
                        hour=task_scheduler_obj.Job_1_Schedule_Hour,
                        minute=task_scheduler_obj.Job_1_Schedule_Minute,
                        second='00', id='period_task', replace_existing=True)


def job_scheduler_start_period():
    scheduler_obj = Scheduler.objects.get(user='admin')
    next_run_job = scheduler_1.get_job('period_task', jobstore='default')
    next_run_date = next_run_job.next_run_time
    scheduled_date = convert_datetime_str(str(next_run_date))
    if verify_dates(scheduled_date, str(scheduler_obj.Date_1)):
            book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_1, scheduler_obj.Password_1,
              scheduler_obj.Time_Slot_1, scheduler_obj.Date_1, scheduler_obj.Email)
    if scheduler_obj.Start_2 and verify_dates(scheduled_date, str(scheduler_obj.Date_2)):
        book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_1, scheduler_obj.Password_1,
              scheduler_obj.Time_Slot_2, scheduler_obj.Date_2, scheduler_obj.Email)
    if scheduler_obj.Start_3 and verify_dates(scheduled_date, str(scheduler_obj.Date_3)):
        book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_2, scheduler_obj.Password_2,
                  scheduler_obj.Time_Slot_3, scheduler_obj.Date_3, scheduler_obj.Email)
    if scheduler_obj.Start_4 and verify_dates(scheduled_date, str(scheduler_obj.Date_4)):
        book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_2, scheduler_obj.Password_2,
                  scheduler_obj.Time_Slot_4, scheduler_obj.Date_4, scheduler_obj.Email)


scheduler_1.add_job(job_scheduler_start_period, 'cron', day_of_week='mon', hour=2,
                    minute=00, second='00', id='period_task', replace_existing=True)
scheduler_1.add_job(job_scheduler_start_now, 'interval', seconds=10, id='start_now_job', replace_existing=True)
scheduler_1.start()
