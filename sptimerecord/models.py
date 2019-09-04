from django.db import models
from splots.models import ParkingSpot
from spusers.models import SmartParkingProfile


class TimeRecord(models.Model):
    user = models.ForeignKey(SmartParkingProfile, on_delete=models.CASCADE)
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    # tiempo que tardo el usuario en estacionar
    time_taked = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
