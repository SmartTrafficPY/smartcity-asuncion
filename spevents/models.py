from django.db import models
from splots.models import ParkingLot, ParkingSpot
from spusers.models import SmartParkingProfile


class Events(models.Model):
    OCUPAR = "O"
    LIBERAR = "L"
    ENTRADA = "E"
    SALIDA = "L"
    ACTION_CHOICES = ((OCUPAR, "Ocupar"), (LIBERAR, "Liberar"), (ENTRADA, "Entrada"), (SALIDA, "Salida"))

    user = models.ForeignKey(SmartParkingProfile, on_delete=models.CASCADE)
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    # time_taked = models.IntegerField(null=True, blank=True)
    # from_app = models.CharField(null=True, blank=True, max_lenght=50)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
