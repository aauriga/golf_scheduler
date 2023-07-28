from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from .views import book_golf
from .models import Scheduler

urlpatterns = [
]

scheduler_1 = BackgroundScheduler()
scheduler_1.add_jobstore(DjangoJobStore(), "default")


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
    book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_1, scheduler_obj.Password_1,
              scheduler_obj.Time_Slot_1, scheduler_obj.Date_1, scheduler_obj.Email)
    if scheduler_obj.Start_2:
        book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_1, scheduler_obj.Password_1,
              scheduler_obj.Time_Slot_2, scheduler_obj.Date_2, scheduler_obj.Email)
    if scheduler_obj.Start_3:
        book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_2, scheduler_obj.Password_2,
                  scheduler_obj.Time_Slot_3, scheduler_obj.Date_3, scheduler_obj.Email)
    if scheduler_obj.Start_4:
        book_golf(scheduler_obj.Website_Url, scheduler_obj.Username_2, scheduler_obj.Password_2,
                  scheduler_obj.Time_Slot_4, scheduler_obj.Date_4, scheduler_obj.Email)


scheduler_1.add_job(job_scheduler_start_period, 'cron', day_of_week='mon', hour=2,
                    minute=00, second='00', id='period_task', replace_existing=True)
scheduler_1.add_job(job_scheduler_start_now, 'interval', seconds=10, id='start_now_job', replace_existing=True)
scheduler_1.start()
