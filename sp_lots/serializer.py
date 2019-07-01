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

    # Foreign Key...

    def to_representation(self, instance):
        self.fields["in_lot"] = LotsSerializers(read_only=True)
        return super(LotsSerializers, self).to_representation(instance)
