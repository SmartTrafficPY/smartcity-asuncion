from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import parsers, renderers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smasu.authentication import (
    IsCreateView,
    IsListView,
    IsRetrieveView,
    IsSuperUserOrStaff,
    TokenAuthenticationInQuery,
)
from smasu.helpers import as_entity
from smasu.models import Application
from smasu.parsers import GeoJSONParser
from smasu.renderers import GeoJSONRenderer
from smevents.models import Event
from smreports.models import SmartMovingEventType
from smrouter.utils import Router

from .models import NavigationRequest
from .serializers import NavigationRequestSerializer


class IsSmartMovingUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.smartmovingprofile is not None


class NavigationRequestView(viewsets.ModelViewSet):
    queryset = NavigationRequest.objects.all()
    serializer_class = NavigationRequestSerializer
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | ((IsListView | IsCreateView | IsRetrieveView) & IsSmartMovingUser),)
    parser_classes = (GeoJSONParser, parsers.FormParser)
    renderer_classes = [GeoJSONRenderer, renderers.BrowsableAPIRenderer]

    @receiver(post_save, sender=NavigationRequest)
    def set(sender, instance, **kwargs):
        router = Router()

        with transaction.atomic():
            if kwargs.get("created", False):
                origin = instance.origin
                destination = instance.destination
                report_types_severe = instance.report_severe
                report_types_light = instance.report_light
                point_init = router.get_point_projected_to_location(origin)
                point_end = router.get_point_projected_to_location(destination)
                instance.origin = point_init
                instance.destination = point_end
                instance.route = router.pedestrian_path(
                    origin, destination, report_types_severe, report_types_light, instance.user_requested
                )
                instance.save()
                Event(
                    application=Application.objects.get(name="SmartMovingApp"),
                    e_type=as_entity(SmartMovingEventType.NAVIGATION_REQUEST),
                    agent=as_entity(instance.user_requested),
                    position=origin,
                ).save()
                pkk = instance.pk
                print(pkk)
        return Response(status=200)
