from django.db import models


class ParkingLot(models.Model):
    radio = models.FloatField()
    lat_center = models.FloatField()
    lng_center = models.FloatField()
    spots_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.username


class ParkingSpot(models.Model):
    PARKING_SPOT_STATUS_CHOICES = (("Free", "F"), ("Occupied", "O"), ("Unknown", "U"))
    in_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    point1_lat = models.FloatField()
    point1_lng = models.FloatField()
    point2_lat = models.FloatField()
    point2_lng = models.FloatField()
    point3_lat = models.FloatField()
    point3_lng = models.FloatField()
    point4_lat = models.FloatField()
    point4_lng = models.FloatField()
    point5_lat = models.FloatField()
    point5_lng = models.FloatField()
    spot_status = models.CharField(max_length=1, choices=PARKING_SPOT_STATUS_CHOICES)
    # user_changed_status = models.ForeignKey(Sp_profiles, on_delete=models.CASCADE)
    status_updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.in_lot
