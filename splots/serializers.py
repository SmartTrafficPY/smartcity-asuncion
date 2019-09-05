from rest_framework import serializers

from .models import ParkingLot, ParkingSpot


class PointSerializer(serializers.Serializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()


class NearbySpotsRequest(serializers.Serializer):
    point = PointSerializer(required=True)
    distance = serializers.FloatField()


class ParkingSpotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = "__all__"


class ParkingLotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ("url", "radio", "name", "center", "created", "modified")

    def get_spot_map(self, obj):
        return [(x.id, x.state) for x in obj.spots.all()]
