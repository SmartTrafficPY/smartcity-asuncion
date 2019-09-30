from rest_framework import serializers

from .models import ParkingLot, ParkingSpot


class NearbySpotsRequest(serializers.Serializer):
    point = serializers.CharField()
    distance = serializers.FloatField(required=False)
    previous_timestamp = serializers.FloatField(required=False, allow_null=True)


class ParkingSpotSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpot
        fields = ("url", "state", "polygon", "lot")

    def get_state(self, spot):
        return spot.get_state()


class ParkingLotSpotSerializer(ParkingSpotSerializer):
    class Meta:
        model = ParkingSpot
        fields = ("url", "state", "polygon")


class ParkingLotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ("url", "name", "center", "geometry", "monitoring_distance")
