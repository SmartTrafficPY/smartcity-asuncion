from django.db import models
from splots.models import ParkingSpot
from spusers.models import SmartParkingProfile


class TimeRecord(models.Model):
    OCUPAR = "O"
    LIBERAR = "L"
    ACTION_CHOICES = ((OCUPAR, "Ocupar"), (LIBERAR, "Liberar"))
    user = models.ForeignKey(SmartParkingProfile, on_delete=models.CASCADE)
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    # tiempo que tardo el usuario en estacionar
    time_taked = models.IntegerField(null=True, blank=True)
    from_app = models.CharField(null=True, blank=True, max_lenght=50)
    action = models.CharField(max_length=16, choices=ACTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
