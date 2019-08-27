from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework import authentication, permissions
from .models import ParkingLot, ParkingSpot
from .serializer import LotsSerializers, SpotSerializers

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


class LotsExtra(APIView):
    """
    View to list all spots in a especific Lot.
    """

    # authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, name, format=None):
        lot = ParkingLot.objects.get(name=name)
        if lot is not None:
            spots = ParkingSpot.objects.all().filter(in_lot=lot.id)
            serializer = SpotSerializers(spots, many=True)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    # def list(self, request, pk, format=None):
    #     spots = ParkingSpot.objects.all().filter(in_lot=pk)
    #     serializer = SpotSerializers(spots, many=True)
    #     return Response(serializer.data)
