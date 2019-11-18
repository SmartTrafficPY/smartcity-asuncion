from datetime import datetime

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.db import transaction
from django.db.models import Count
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from rest_framework import parsers, renderers, serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from smasu.authentication import IsRetrieveView, IsCreateView ,IsSafeReadOnlyView, IsSuperUserOrStaff, TokenAuthenticationInQuery
from smasu.helpers import as_entity
from smasu.models import Application
from smevents.models import Event
from .parsers import ReportPoiGeoJSONParser
from .renderers import ReportPoiGeoJSONRenderer
from .helpers import SmartMovingCacheHelper
from .serializers import ReportPoiSerializer, ContributionSerializer
from .models import ReportPoi, ReportType, Contribution, SmartMovingEventType
from django.dispatch import receiver


class IsSmartMovingUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.smartmovingprofile is not None


class ReportsPoiView(viewsets.ModelViewSet):
    queryset = ReportPoi.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | (IsCreateView & IsSmartMovingUser),)
    parser_classes = (ReportPoiGeoJSONParser, parsers.FormParser)
    serializer_class = ReportPoiSerializer
    renderer_classes = [ReportPoiGeoJSONRenderer, renderers.BrowsableAPIRenderer]

    @receiver(post_save, sender=ReportPoi)
    def create_event_report(sender,instance, **kwargs):
        with transaction.atomic():
            if kwargs.get('created', False):
                Event(
                    application=Application.objects.get(name="SmartMovingApp"),
                    e_type=as_entity(SmartMovingEventType.CREATED_REPORT_POI),
                    agent=as_entity(instance.user_created),
                    position=instance.coordinates_poi,
                ).save()
        return Response(status=200)


class ContributionReportPoiView(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthenticationInQuery)
    permission_classes = (IsSuperUserOrStaff | (IsCreateView & IsSmartMovingUser),)
    serializer_class = ContributionSerializer

    @receiver(post_save, sender=Contribution)
    def create_event(sender,instance, **kwargs):
        
        with transaction.atomic():
            if kwargs.get('created', False):
                Event(
                    application=Application.objects.get(name="SmartMovingApp"),
                    e_type=as_entity(SmartMovingEventType.MODIFIED_REPORT_POI),
                    agent=as_entity(instance.user),
                    position= instance.reportpoi.coordinates_poi,
                    #extra_information = reportid,
                ).save()
        return Response(status=200)



    