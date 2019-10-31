from django.contrib import admin
from smasu.admin import SmartTrafficOSMGeoAdmin
from .models import ReportPoi, ReportType, Contribution

# Register your models here.

admin.site.register(ReportPoi, SmartTrafficOSMGeoAdmin)


admin.site.register(ReportType, SmartTrafficOSMGeoAdmin)

class SmartMovingContribution(admin.ModelAdmin):
    pass

admin.site.register(Contribution, SmartMovingContribution)