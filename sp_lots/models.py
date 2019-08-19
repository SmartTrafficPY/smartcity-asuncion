from django.db import models


class ParkingLot(models.Model):
    radio = models.FloatField(blank=False)
    latitud_center = models.FloatField(blank=False)
    longitud_center = models.FloatField(blank=False)
    spots_in = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ParkingSpot(models.Model):
    FREE = "F"
    OCCUPIED = "O"
    UNKNOWN = "U"
    PARKING_SPOT_STATUS_CHOICES = ((FREE, "Free"), (OCCUPIED, "Occupied"), (UNKNOWN, "Unknown"))

    in_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    p1_latitud = models.FloatField()
    p1_longitud = models.FloatField()
    p2_latitud = models.FloatField()
    p2_longitud = models.FloatField()
    p3_latitud = models.FloatField()
    p3_longitud = models.FloatField()
    p4_latitud = models.FloatField()
    p4_longitud = models.FloatField()
    p5_latitud = models.FloatField()
    p5_longitud = models.FloatField()
    status = models.CharField(max_length=15, choices=PARKING_SPOT_STATUS_CHOICES)
    # user_changed_status = models.ForeignKey(Sp_profiles, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
