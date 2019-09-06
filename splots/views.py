from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from smasu.authentication import IsRetrieveView, IsSuperUserOrStaff, TokenAuthenticationInQuery

from .models import ParkingLot, ParkingSpot
from .serializers import NearbySpotsRequest, ParkingLotSerializer, ParkingSpotSerializer


class IsSmartParkingUser(IsAuthenticated):
    def has_permission(self, request, view):
        profile = request.user.smartparkingprofile
        return super().has_permission(request, view) and profile is not None


class IsSafeReadOnlyView(BasePermission):
    def has_permission(self, request, view):
        return view.action in {"list", "retrieve"}


class ParkingLotView(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | (IsSafeReadOnlyView & IsAuthenticated),)

    @action(methods=["get"], detail=True, permission_classes=(IsAuthenticated,))
    def spots(self, request, pk=None):
        lots = ParkingSpot.objects.filter(parking_lot=pk).all()
        return Response({x.pk: x.state for x in lots})


class ParkingSpotView(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | (IsRetrieveView & IsSmartParkingUser),)

    def get_serializer_class(self):
        if self.action in {"set", "reset"}:
            return serializers.Serializer

        elif self.action == "nearby":
            return NearbySpotsRequest

        return ParkingSpotSerializer

    @action(methods=["post"], detail=True, permission_classes=(IsSuperUserOrStaff | IsSmartParkingUser,))
    def set(self, request, pk, format=None):
        try:
            spot = ParkingSpot.objects.get(pk=pk)
        except ParkingSpot.DoesNotExist:
            return Response(status=404)

        spot.state = ParkingSpot.STATE_OCCUPIED
        spot.save()
        return Response(status=200)

    @action(methods=["post"], detail=True, permission_classes=(IsSuperUserOrStaff | IsSmartParkingUser,))
    def reset(self, request, pk, format=None):
        spot = ParkingSpot.objects.get(pk=pk)
        spot.state = ParkingSpot.STATE_FREE
        spot.save()
        return Response(status=200)

    @action(methods=["post"], detail=False, permission_classes=(IsSuperUserOrStaff | IsSmartParkingUser,))
    def nearby(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        point_data = serializer.validated_data["point"]
        distance = serializer.validated_data.get("distance", settings.NEARBY_SPOTS_DEFAULT_DISTANCE)

        nearby_spots = ParkingSpot.objects.filter(
            polygon__distance_lte=(Point(x=point_data["lon"], y=point_data["lat"]), D(m=distance))
        )

        return Response({x.pk: x.state for x in nearby_spots})