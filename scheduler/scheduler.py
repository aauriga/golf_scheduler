from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from .views import book_golf
from .models import Scheduler

urlpatterns = [
]

scheduler_1 = BackgroundScheduler()
scheduler_1.add_jobstore(DjangoJobStore(), "default")
scheduler_2 = BackgroundScheduler()


def job_scheduler_start_now():
    task_scheduler_obj = Scheduler.objects.get(user='admin')
    scheduled_time = str(scheduler_1.get_job('period_task').next_run_time)
    # if scheduled_time[11:13] != get_schedule_hour(task_scheduler_obj) or scheduled_time[14:16] != get_schedule_minute(
    #         task_scheduler_obj):
    scheduler_1.add_job(job_scheduler_start_period, 'cron', day_of_week=task_scheduler_obj.Job_1_Schedule_Hour,
                        hour=task_scheduler_obj.Job_1_Schedule_Hour,
                        minute=task_scheduler_obj.Job_1_Schedule_Hour,
                        second='00', id='period_task', replace_existing=True)
    print(task_scheduler_obj.Job_2_Start)
    if task_scheduler_obj.Job_2_Start:
        scheduler_1.add_job(job_scheduler_start_period, 'cron', day_of_week=task_scheduler_obj.Job_2_Schedule_Hour,
                            hour=task_scheduler_obj.Job_2_Schedule_Hour,
                            minute=task_scheduler_obj.Job_2_Schedule_Hour,
                            second='00', id='period_task_2', replace_existing=True)
    else:
        try:
            scheduler_1.remove_job('period_task_2')
        except:
            pass


def job_scheduler_start_period():
    scheduler_obj = Scheduler.objects.get(user='admin')
    book_golf(scheduler_obj.Website_Url, scheduler_obj.Username, scheduler_obj.Password,
              scheduler_obj.Time_Slot, scheduler_obj.Date, scheduler_obj.Email)


scheduler_1.add_job(job_scheduler_start_period, 'cron', day_of_week='mon', hour=2,
                    minute=00, second='00', id='period_task', replace_existing=True)
scheduler_1.add_job(job_scheduler_start_now, 'interval', seconds=10, id='start_now_job', replace_existing=True)
scheduler_1.start()
