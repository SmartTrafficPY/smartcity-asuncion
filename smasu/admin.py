from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Application


class SmartTrafficOSMGeoAdmin(OSMGeoAdmin):
    map_template = "gis/admin/smarttraffic_osm.html"


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Application, ApplicationAdmin)
