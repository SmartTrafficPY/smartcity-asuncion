from django.conf import settings
from django.contrib.gis.db.models import PointField, PolygonField
from django.db import models
from django.utils import timezone


class ParkingLot(models.Model):
    radio = models.FloatField(blank=False)
    name = models.CharField(max_length=50)

    center = PointField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} - {self.name}"


class ParkingSpot(models.Model):
    STATE_FREE = "F"
    STATE_OCCUPIED = "O"
    STATE_UNKNOWN = "U"
    STATE_CHOICES = ((STATE_FREE, "Free"), (STATE_OCCUPIED, "Occupied"), (STATE_UNKNOWN, "Unknown"))

    lot = models.ForeignKey(ParkingLot, related_name="spots", on_delete=models.CASCADE)
    state = models.CharField(max_length=15, choices=STATE_CHOICES, default=STATE_UNKNOWN)

    polygon = PolygonField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_state(self):
        elapsed = timezone.now() - self.modified
        if elapsed > settings.SPOT_STATE_EXPIRATION_TIME:
            return ParkingSpot.STATE_UNKNOWN

        return self.state

    def __str__(self):
        return f"{self.pk} - Lot({self.lot})"
