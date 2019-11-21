from django.contrib import admin

from .models import SmartParkingProfile


class SmartParkingProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(SmartParkingProfile, SmartParkingProfileAdmin)
