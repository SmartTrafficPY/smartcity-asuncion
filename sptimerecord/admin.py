from django.contrib import admin

from .models import TimeRecord


class TimeRecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(TimeRecord, TimeRecordAdmin)
