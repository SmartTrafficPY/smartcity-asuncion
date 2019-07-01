import datetime

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework import authentication, permissions
from .models import ParkingLot, ParkingSpot
from .serializer import LotsSerializers, SpotSerializers

# DOCS:
# https://docs.djangoproject.com/en/2.2/topics/http/views/
# https://docs.djangoproject.com/en/2.2/topics/http/decorators/
# https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/
# REST_FRAMEWORK:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#tutorial-3-class-based-views


class LotsList(APIView):
    # Class view for Return List types of responses...

    def get(self, request, format=None):
        lots = ParkingLot.objects.all()
        serializer = LotsSerializers(lots, many=True)
        return Response(serializer.data)


class LotsCRUD(APIView):
    """
    Set Create, Read, Update and Delete services of SmartParking users profile
    View to list all users in the system.
    * Should requires token authentication.
    * Only some users should able to access this view.
    """

    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get_object_id(self, id):
        try:
            return ParkingLot.objects.get(id=id)
        except ParkingLot.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        perfil_sp = self.get_object_id(id)
        serializer = LotsSerializers(perfil_sp)
        return Response(serializer.data)

    def post(self, request, format=None):
        # if not exist that alias in another profile, you can insert it in the DB...
        try:
            ParkingLot.objects.get(id=request.data.get("id"))
        except ParkingLot.DoesNotExist:
            query_insert = ParkingLot(
                radio=request.POST.get("password"),
                lat_center=request.POST.get("lat_center"),
                lng_center=request.POST.get("lng_center"),
                spots_in=request.POST.get("spots_in"),
                created_at=current_datetime(),
                updated_at=current_datetime(),
            )
            query_insert.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response("This profile already exists", status=status.HTTP_403_FORBIDDEN)

    def put(self, request, format=None):
        # if exist that alias Profile, update else conflict...
        # for now let you to update the password...
        try:
            lots = ParkingLot.objects.get(id=request.data.get("id"))
        except ParkingLot.DoesNotExist:
            return Response("This alias profile does not exists", status=status.HTTP_404_NOT_FOUND)
        else:
            # Should be worth it change the center and radious of lot?
            lots.spots_in = lots.spots_in + 1
            lots.updated_at = current_datetime()
            lots.save()
            return Response(request.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, format=None):
        lot = self.get_object_id(id)
        lot.delete()
        return Response(status=status.HTTP_200_OK)


class SpotsList(APIView):
    # Class view for Return List types of responses...

    def get(self, request, format=None):
        spot = ParkingSpot.objects.all()
        serializer = SpotSerializers(spot, many=True)
        return Response(serializer.data)


class SpotsCRUD(APIView):
    """
    Set Create, Read, Update and Delete services of SmartParking users profile
    View to list all users in the system.
    * Should requires token authentication.
    * Only some users should able to access this view.
    """

    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get_object_id(self, id):
        try:
            return ParkingSpot.objects.get(id=id)
        except ParkingSpot.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        spot = self.get_object_id(id)
        serializer = SpotSerializers(spot)
        return Response(serializer.data)

    def post(self, request, format=None):
        # a resumed way to put it...
        serializer = SpotSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, format=None):
        # if exist that id ParkingSpot, update status, user who changed it...
        try:
            spot = ParkingSpot.objects.get(id=request.data.get("id"))
        except ParkingSpot.DoesNotExist:
            return Response("This alias profile does not exists", status=status.HTTP_404_NOT_FOUND)
        else:
            spot.spot_status = request.data.get("status")
            # spot.user_changed_status = request.data.get("user_changed_status")
            spot.status_updated_at = current_datetime()
            spot.save()
            return Response(request.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, format=None):
        spot = self.get_object_id(id)
        spot.delete()
        return Response(status=status.HTTP_200_OK)


def current_datetime():
    now = datetime.datetime.now()
    return now
