from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from smasu.authentication import IsCreateView, TokenAuthenticationInQuery
from splots.views import IsSmartParkingUser, IsSuperUserOrStaff

from .models import Events
from .serializer import EventsSerializer


class EventsViews(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | (IsCreateView & IsSmartParkingUser),)
