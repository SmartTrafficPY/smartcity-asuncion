from django.contrib import admin
from smasu.admin import SmartTrafficOSMGeoAdmin

from .models import Report, ReportType, StatusUpdate

# Register your models here.

admin.site.register(Report, SmartTrafficOSMGeoAdmin)


admin.site.register(ReportType, SmartTrafficOSMGeoAdmin)


class SmartMovingStatusUpdate(admin.ModelAdmin):
    pass


admin.site.register(StatusUpdate, SmartMovingStatusUpdate)
