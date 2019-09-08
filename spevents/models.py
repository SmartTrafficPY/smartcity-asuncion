from django.db import models
from splots.models import ParkingLot
from spusers.models import SmartParkingProfile


class Events(models.Model):
    OCUPAR = "O"
    LIBERAR = "L"
    ENTRADA = "E"
    SALIDA = "S"
    ACTION_CHOICES = ((OCUPAR, "Ocupar"), (LIBERAR, "Liberar"), (ENTRADA, "Entrada"), (SALIDA, "Salida"))

    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    user = models.ForeignKey(SmartParkingProfile, on_delete=models.CASCADE)

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"
