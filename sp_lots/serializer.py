from rest_framework import serializers

from .models import ParkingLot, ParkingSpot

# https://docs.djangoproject.com/en/2.2/topics/serialization/


class LotsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = "__all__"


class SpotSerializers(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = "__all__"
