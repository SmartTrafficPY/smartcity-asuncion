from django.contrib.gis import admin
from smasu.admin import SmartTrafficOSMGeoAdmin

from .models import ParkingLot, ParkingSpot

admin.site.register(ParkingLot, SmartTrafficOSMGeoAdmin)
admin.site.register(ParkingSpot, SmartTrafficOSMGeoAdmin)
