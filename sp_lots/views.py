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
    Create, Read, Update and Delete services of SmartParking parking lots
    View to list all lots in the system.
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
        # if not exist that id, you can insert it in the DB...
        try:
            ParkingLot.objects.get(id=request.data.get("id"))
        except ParkingLot.DoesNotExist:
            query_insert = ParkingLot(
                radio=request.POST.get("radio"),
                lat_center=request.POST.get("lat_center"),
                lng_center=request.POST.get("lng_center"),
                # First time should be 0 ?
                spots_in=0,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            query_insert.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response("This lot already exists", status=status.HTTP_403_FORBIDDEN)

    def put(self, request, format=None):
        # if exist that parking spot id, update else conflict...
        try:
            lots = ParkingLot.objects.get(id=request.data.get("id"))
        except ParkingLot.DoesNotExist:
            return Response("This parking lot does not exists", status=status.HTTP_404_NOT_FOUND)
        else:
            # Should be worth it change the center and radious of lot?
            lots.radio = request.data.get("radio")
            lots.lat_center = request.data.get("lat_center")
            lots.lng_center = request.data.get("lng_center")
            lots.updated_at = datetime.datetime.now()
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
    Create, Read, Update and Delete services of SmartParking parking spots
    View to list all spots in the system.
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
        # if not exist that id , you can insert it in the DB...
        try:
            ParkingSpot.objects.get(id=request.data.get("id"))
        except ParkingSpot.DoesNotExist:
            try:
                lot_fk = ParkingLot.objects.get(id=request.POST.get("in_lot"))
            except ParkingLot.DoesNotExist:
                return Response("This lot id do not exists", status=status.HTTP_404_NOT_FOUND)
            else:
                query_insert = ParkingSpot(
                    in_lot=lot_fk,
                    point1_lat=request.POST.get("point1_lat"),
                    point1_lng=request.POST.get("point1_lng"),
                    point2_lat=request.POST.get("point2_lat"),
                    point2_lng=request.POST.get("point2_lng"),
                    point3_lat=request.POST.get("point3_lat"),
                    point3_lng=request.POST.get("point3_lng"),
                    point4_lat=request.POST.get("point4_lat"),
                    point4_lng=request.POST.get("point4_lng"),
                    point5_lat=request.POST.get("point5_lat"),
                    point5_lng=request.POST.get("point5_lng"),
                    spot_status="U",
                    status_updated_at=datetime.datetime.now(),
                    created_at=datetime.datetime.now(),
                )
                query_insert.save()
                lot_fk.spots_in += 1
                # should add +1 to spots_in in this objet instance...
                lot_fk.save()
                return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response("This parking spot already exists", status=status.HTTP_403_FORBIDDEN)

    def put(self, request, format=None):
        # if exist that id ParkingSpot, update status, user who changed it...
        # We could change the lot_id to?
        try:
            spot = ParkingSpot.objects.get(id=request.data.get("id"))
        except ParkingSpot.DoesNotExist:
            return Response("This parking spot does not exists", status=status.HTTP_404_NOT_FOUND)
        else:
            # spot.in_lot = request.data.get("in_lot")
            spot.spot_status = request.data.get("spot_status")
            # spot.user_changed_status = request.data.get("user_changed_status")
            spot.status_updated_at = datetime.datetime.now()
            spot.save()
            return Response(request.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, format=None):
        spot = self.get_object_id(id)
        spot.delete()
        return Response(status=status.HTTP_200_OK)
