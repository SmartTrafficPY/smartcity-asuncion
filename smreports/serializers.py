from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import timezone
from smevents.models import Event

from .parsers import ReportPoiGeoJSONParser
from .renderers import ReportPoiGeoJSONRenderer
from .helpers import SmartMovingCacheHelper
from smasu.helpers import as_entity
from smasu.models import Application
from .models import ReportPoi, ReportType, Contribution, SmartMovingEventType



class ReportPoiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReportPoi
        fields = ("url", "pk", "user_created","report_type", "coordinates_poi", "modified" )
    
    def create(self, validated_data):

        with transaction.atomic():

            instance = ReportPoi.objects.create(**validated_data)
        
        instance = ReportPoi.objects.get(pk=instance.pk)
        return instance

class ContributionSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Contribution
        fields = ("pk","reportpoi","user","value","created")
    
    def create(self, validated_data):

        with transaction.atomic():
            
            instance = Contribution.objects.create(**validated_data)
            reportpoid = instance.reportpoi
            reportpoid.modified = instance.created
            reportpoid.save()        
        return instance