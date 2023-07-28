from django.contrib import admin

from .models import Scheduler


# Register your models here.
@admin.register(Scheduler)
class SchedulerAdmin(admin.ModelAdmin):
    list_display = ['title', 'Date', 'Time_Slot']

    search_fields = ['title']