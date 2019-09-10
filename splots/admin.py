from django.contrib.gis import admin

from .models import ParkingLot, ParkingSpot

admin.site.register(ParkingLot, admin.GeoModelAdmin)
admin.site.register(ParkingSpot, admin.GeoModelAdmin)
