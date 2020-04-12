from django.contrib.gis.geos import Point
from rest_framework import serializers
from smrouter.utils import Router
from ucusers.models import UcarpoolingProfile
from ucusers.serializers import ProfileSerializer

from .models import Carpool, CarpoolRating, ItineraryRoute, RequestCarpool, UserItinerary


class UserItinerarySerializer(serializers.ModelSerializer):
    """ Serializer for the UserItinerary model """

    class Meta:

        """ For which model this serializer belongs to """

        model = UserItinerary

        fields = ("id", "isDriver", "origin", "destination", "timeOfArrival", "timeOfDeparture")

        read_only_fields = ("id",)

    def itineraryParser(self, data):
        """Converting the input fields into Python objects"""

        data["ucarpoolingProfile"] = UcarpoolingProfile.objects.get(user_id=self.context["request"].user.pk)

        """Serializing the Origin and Destination fields into PointFields"""
        if "origin" in data:
            latitude, longitude = data["origin"].split(",")
            origin = Point(float(longitude), float(latitude))
            data["origin"] = origin

        if "destination" in data:
            latitude, longitude = data["destination"].split(",")
            destination = Point(float(longitude), float(latitude))
            data["destination"] = destination

        return data

    def create(self, validated_data):

        data_to_save = self.itineraryParser(validated_data)
        itinerary_created = UserItinerary.objects.create(**data_to_save)

        """Si es chofer, guarda la trayectoria al destino para calculos posteriores"""
        if itinerary_created.isDriver:
            router = Router()
            path = router.driver_path(origin=itinerary_created.origin, destination=itinerary_created.destination)
            # Guardar en el modelo ItineraryRoute
            ItineraryRoute.objects.create(
                itinerary=itinerary_created,
                pathLatitude=path["lat"],
                pathLongitude=path["lon"],
                aggCost=path["agg_cost"],
            )

        """ Create a new user with encypted password and return it """
        return itinerary_created

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

        fields = ("id", "driver", "poolers", "route")

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


class CarpoolRatingSerializer(serializers.ModelSerializer):
    """ Serializer for the CarpoolRating model """

    qualified = serializers.PrimaryKeyRelatedField(queryset=UcarpoolingProfile.objects.all())

    subject = serializers.PrimaryKeyRelatedField(queryset=Carpool.objects.all())

    class Meta:

        model = CarpoolRating

        fields = ("id", "qualified", "subject")

        read_only_fields = ("id",)


class CarpoolRatingDetailSerializer(CarpoolRatingSerializer):
    """Serializer for detailed CarpoolRating"""

    qualified = ProfileSerializer()
    subject = CarpoolDetailSerializer()
