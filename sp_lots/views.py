from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

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


class LotsView(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = LotsSerializers
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    # permission_classes = (IsAuthenticated,)
