from rest_framework import viewsets

from .models import ParkingLot


class ParkingLotView(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    # serializer_class = UserSerializer
    # authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    # permission_classes = (
    #     IsSuperUserOrStaff
    #     | ((IsListView | IsCreateView) & IsSmartParkingApp)
    #     | (~(IsListView | IsCreateView) & IsSameUser),
    # )
