from django.db import transaction
from rest_framework import serializers

from .models import ParkingLot, ParkingSpot

# https://docs.djangoproject.com/en/2.2/topics/serialization/


class SpotSerializers(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = "__all__"

    def create(self, validated_data):

        with transaction.atomic():
            instance = ParkingSpot.objects.create(**validated_data)
            lot_data = ParkingLot.objects.get(pk=instance.in_lot.pk)
            lot_data.spots_in = lot_data.spots_in + 1
            lot_data.save()

        instance = ParkingSpot.objects.get(pk=instance.pk)
        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.save()

        instance = ParkingSpot.objects.get(pk=instance.pk)
        return instance


class LotsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = "__all__"

    def create(self, validated_data):

        with transaction.atomic():
            instance = ParkingLot.objects.create(**validated_data)

        instance = ParkingLot.objects.get(pk=instance.pk)
        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.save()

        instance = ParkingLot.objects.get(pk=instance.pk)
        return instance
