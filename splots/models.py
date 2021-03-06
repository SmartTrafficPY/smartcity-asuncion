from enum import Enum

from django.conf import settings
from django.contrib.gis.db.models import GeometryField, PointField, PolygonField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

SmartParkingEventType = Enum("SmartParkingEventType", "OCCUPY_SPOT FREE_SPOT ENTER_LOT EXIT_LOT")
SmartParkingEventType.as_entity = lambda self: reverse("entities:smartparking_event_types", args=(slugify(self.name),))


class ParkingLot(models.Model):
    monitoring_distance = models.FloatField(blank=False)
    name = models.CharField(max_length=50)

    center = PointField()

    geometry = GeometryField(blank=True, null=True, default=None)

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
