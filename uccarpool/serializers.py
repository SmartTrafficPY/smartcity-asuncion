from django.contrib.gis.geos import Point
from rest_framework import serializers
from ucusers.models import UcarpoolingProfile
from ucusers.serializers import ProfileSerializer

from .models import Carpool, RequestCarpool, UserItinerary


class UserItinerarySerializer(serializers.ModelSerializer):
    """ Serializer for the UserItinerary model """

    class Meta:

        """ For which model this serializer belongs to """

        model = UserItinerary

        fields = ("id", "isDriver", "origin", "destination", "timeOfArrival", "timeOfDeparture")

        read_only_fields = ("id",)

    def itineraryParser(self, data):
        """Converting the input fields into Python objects"""

        request_ucarpoolingProfile = UcarpoolingProfile.objects.get(user_id=self.context["request"].user.pk)
        data["ucarpoolingProfile"] = request_ucarpoolingProfile

        """Serializing the Origin and Destination fields into PointFields"""
        if "origin" in data:
            latitude, longitude = data["origin"].split(",")
            origin = Point(float(latitude), float(longitude))
            data["origin"] = origin

        if "destination" in data:
            latitude, longitude = data["destination"].split(",")
            destination = Point(float(latitude), float(longitude))
            data["destination"] = destination

        return data

    def create(self, validated_data):

        data_to_save = self.itineraryParser(validated_data)

        """ Create a new user with encypted password and return it """
        return UserItinerary.objects.create(**data_to_save)

    def update(self, instance, validated_data):
        """Converting the PUT fields into Python objects"""

        data_to_save = self.itineraryParser(validated_data)

        return super().update(instance, data_to_save)


class CarpoolSerializer(serializers.ModelSerializer):
    """ Serializer for the UserItinerary model """

    driver = serializers.PrimaryKeyRelatedField(queryset=UcarpoolingProfile.objects.all())

    poolers = serializers.PrimaryKeyRelatedField(many=True, queryset=UcarpoolingProfile.objects.all())

    class Meta:

        model = Carpool

        fields = ("id", "driver", "poolers", "carpoolItinerary")

        read_only_fields = ("id",)


class CarpoolDetailSerializer(CarpoolSerializer):
    """Serializer for detailed Carpool"""

    driver = ProfileSerializer()
    poolers = ProfileSerializer(many=True, read_only=True)


class RequestCarpoolSerializer(serializers.ModelSerializer):
    """ Serializer for the RequestCarpool model """

    recipient = serializers.PrimaryKeyRelatedField(queryset=UcarpoolingProfile.objects.all())

    subject = serializers.PrimaryKeyRelatedField(queryset=Carpool.objects.all())

    class Meta:

        model = RequestCarpool

        fields = ("id", "recipient", "subject")

        read_only_fields = ("id",)


class RequestCarpoolDetailSerializer(RequestCarpoolSerializer):
    """Serializer for detailed RequestCarpool"""

    recipient = ProfileSerializer()
    subject = CarpoolDetailSerializer()
