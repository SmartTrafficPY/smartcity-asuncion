from rest_framework import serializers

from .models import ParkingLot, ParkingSpot


class PointSerializer(serializers.Serializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()


class NearbySpotsRequest(serializers.Serializer):
    point = PointSerializer()
    distance = serializers.FloatField(required=False)
    previous_timestamp = serializers.FloatField(required=False)


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
        fields = ("url", "radio", "name", "center")
