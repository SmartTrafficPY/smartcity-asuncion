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

        instance.status = validated_data.get("status", instance.status)
        instance.in_lot = validated_data.get("in_lot", instance.in_lot)

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

        instance.radio = validated_data.get("radio", instance.radio)
        instance.latitud_center = validated_data.get("latitud_center", instance.latitud_center)
        instance.longitud_center = validated_data.get("longitud_center", instance.longitud_center)

        with transaction.atomic():
            instance.save()

        instance = ParkingLot.objects.get(pk=instance.pk)
        return instance
