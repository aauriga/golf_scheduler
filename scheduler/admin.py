from django.contrib import admin

from .models import Scheduler


# Register your models here.
@admin.register(Scheduler)
class SchedulerAdmin(admin.ModelAdmin):
    list_display = ['title', 'Date_1', 'Time_Slot_1']

    search_fields = ['title']