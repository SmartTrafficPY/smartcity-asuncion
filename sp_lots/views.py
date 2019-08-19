from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response

# from rest_framework import authentication, permissions
from .models import ParkingLot, ParkingSpot
from .serializer import LotsSerializers, SpotSerializers

# DOCS:
# https://docs.djangoproject.com/en/2.2/topics/http/views/
# https://docs.djangoproject.com/en/2.2/topics/http/decorators/
# https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/
# REST_FRAMEWORK:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#tutorial-3-class-based-views


# from rest_framework.decorators import detail_route


class SpotsView(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = SpotSerializers
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        spots = ParkingSpot.objects.all().filter(in_lot=pk)
        serializer = LotsSerializers(spots, many=True)
        return Response(serializer.data)


class LotsView(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = LotsSerializers
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        lots = ParkingLot.objects.all()
        serializer = LotsSerializers(lots, many=True)
        return Response(serializer.data)
