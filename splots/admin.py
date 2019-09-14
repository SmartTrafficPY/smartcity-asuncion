from django.contrib.gis import admin

from .models import ParkingLot, ParkingSpot


class SmartTrafficOSMGeoAdmin(admin.OSMGeoAdmin):
    map_template = "gis/admin/smarttraffic_osm.html"


admin.site.register(ParkingLot, admin.GeoModelAdmin)
admin.site.register(ParkingSpot, SmartTrafficOSMGeoAdmin)
