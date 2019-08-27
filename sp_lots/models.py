from django.db import models


class ParkingLot(models.Model):
    radio = models.FloatField(blank=False)
    name = models.CharField(max_length=50)
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
    p1_latitud = models.FloatField(null=False, blank=False)
    p1_longitud = models.FloatField(null=False, blank=False)
    p2_latitud = models.FloatField(null=False, blank=False)
    p2_longitud = models.FloatField(null=False, blank=False)
    p3_latitud = models.FloatField(null=False, blank=False)
    p3_longitud = models.FloatField(null=False, blank=False)
    p4_latitud = models.FloatField(null=False, blank=False)
    p4_longitud = models.FloatField(null=False, blank=False)
    p5_latitud = models.FloatField(null=False, blank=False)
    p5_longitud = models.FloatField(null=False, blank=False)
    status = models.CharField(max_length=15, choices=PARKING_SPOT_STATUS_CHOICES, default="U")
    # user_changed_status = models.ForeignKey(Sp_profiles, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
