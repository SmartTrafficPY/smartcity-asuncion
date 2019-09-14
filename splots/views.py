from datetime import datetime

from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db import transaction
from django.db.models import Q
from django.utils.timezone import make_aware, now
from rest_framework import parsers, renderers, serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smasu.authentication import IsRetrieveView, IsSafeReadOnlyView, IsSuperUserOrStaff, TokenAuthenticationInQuery
from smasu.helpers import as_entity
from smasu.models import Application
from smasu.parsers import NearbyGeoJSONParser
from smasu.renderers import NearbyGeoJSONRenderer
from smevents.models import Event

from .helpers import SmartParkingCacheHelper
from .models import ParkingLot, ParkingSpot, SmartParkingEventType
from .parsers import ParkingSpotGeoJSONParser
from .renderers import ParkingLotGeoJSONRenderer, ParkingSpotGeoJSONRenderer
from .serializers import NearbySpotsRequest, ParkingLotSerializer, ParkingLotSpotSerializer, ParkingSpotSerializer


class IsSmartParkingUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.smartparkingprofile is not None


def as_state_map(spots):
    return {x.pk: x.get_state() for x in spots}


class ParkingLotView(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | (IsSafeReadOnlyView & IsAuthenticated),)
    renderer_classes = [ParkingLotGeoJSONRenderer, renderers.BrowsableAPIRenderer]

    @action(
        methods=["get"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        renderer_classes=[renderers.JSONRenderer, ParkingSpotGeoJSONRenderer, renderers.BrowsableAPIRenderer],
    )
    def spots(self, request, pk=None, format=None):
        spots = ParkingSpot.objects.filter(lot=pk)
        if isinstance(request.accepted_renderer, ParkingSpotGeoJSONRenderer):
            return Response((ParkingLotSpotSerializer(x, context={"request": request}).data for x in spots))

        return Response(as_state_map(spots))


class ParkingSpotView(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | (IsRetrieveView & IsSmartParkingUser),)
    parser_classes = (ParkingSpotGeoJSONParser, parsers.JSONParser, parsers.FormParser)
    renderer_classes = [ParkingSpotGeoJSONRenderer, renderers.BrowsableAPIRenderer]

    def get_serializer_class(self):
        if self.action in {"set", "reset"}:
            return serializers.Serializer

        elif self.action == "nearby":
            return NearbySpotsRequest

        return ParkingSpotSerializer

    @action(methods=["post"], detail=True, permission_classes=(IsSuperUserOrStaff | IsSmartParkingUser,))
    def set(self, request, pk, format=None):
        with transaction.atomic():
            try:
                spot = ParkingSpot.objects.get(pk=pk)
            except ParkingSpot.DoesNotExist:
                return Response(status=404)

            spot.state = ParkingSpot.STATE_OCCUPIED
            spot.save()

            Event(
                application=SmartParkingCacheHelper.get_object("application", Application, {"name": "smartparking"}),
                e_type=as_entity(SmartParkingEventType.OCCUPY_SPOT),
                agent=as_entity(request.user),
                position=spot.polygon.centroid,
            ).save()

        return Response(status=200)

    @action(methods=["post"], detail=True, permission_classes=(IsSuperUserOrStaff | IsSmartParkingUser,))
    def reset(self, request, pk, format=None):
        with transaction.atomic():
            try:
                spot = ParkingSpot.objects.get(pk=pk)
            except ParkingSpot.DoesNotExist:
                return Response(status=404)

            spot.state = ParkingSpot.STATE_FREE
            spot.save()

            Event(
                application=SmartParkingCacheHelper.get_object("application", Application, {"name": "smartparking"}),
                e_type=as_entity(SmartParkingEventType.FREE_SPOT),
                agent=as_entity(request.user),
                position=spot.polygon.centroid,
            ).save()

        return Response(status=200)

    @action(
        methods=["post"],
        detail=False,
        permission_classes=(IsSuperUserOrStaff | IsSmartParkingUser,),
        parser_classes=(NearbyGeoJSONParser, parsers.JSONParser, parsers.FormParser),
        renderer_classes=[NearbyGeoJSONRenderer, renderers.JSONRenderer, renderers.BrowsableAPIRenderer],
    )
    def nearby(self, request, format=None):
        serializer = self.get_serializer_class()(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        point_data = serializer.validated_data["point"]
        distance = serializer.validated_data.get("distance", settings.NEARBY_SPOTS_DEFAULT_DISTANCE)

        query = [Q(polygon__distance_lte=(Point(x=point_data["lon"], y=point_data["lat"]), D(m=distance)))]

        previous_timestamp = serializer.validated_data.get("previous_timestamp")
        if previous_timestamp:
            query = [Q(modified__gt=make_aware(datetime.fromtimestamp(previous_timestamp)))] + query

        nearby_spots = ParkingSpot.objects.filter(*query)
        if isinstance(request.accepted_renderer, NearbyGeoJSONRenderer):
            return Response(
                (ParkingSpotSerializer(x, context={"request": request}).data for x in nearby_spots),
                headers={"X-Timestamp": now().timestamp()},
            )

        return Response(as_state_map(nearby_spots), headers={"X-Timestamp": now().timestamp()})
