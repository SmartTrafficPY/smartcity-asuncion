from rest_framework import parsers, renderers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from smasu.authentication import IsCreateView, IsSuperUserOrStaff, TokenAuthenticationInQuery

from .models import Event
from .parsers import EventGeoJSONParser
from .renderers import EventGeoJSONRenderer
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    parser_classes = (EventGeoJSONParser, parsers.FormParser)
    permission_classes = (IsSuperUserOrStaff | (IsCreateView & IsAuthenticated),)
    renderer_classes = [EventGeoJSONRenderer, renderers.BrowsableAPIRenderer]
