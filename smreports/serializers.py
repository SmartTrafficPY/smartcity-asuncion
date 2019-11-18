from django.db import transaction
from rest_framework import serializers

from .models import Contribution, ReportPoi


class ReportPoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPoi
        fields = ("url", "user_created", "report_type", "modified", "status", "coordinates_poi")

    def create(self, validated_data):

        with transaction.atomic():

            instance = ReportPoi.objects.create(**validated_data)

        instance = ReportPoi.objects.get(pk=instance.pk)
        return instance


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ("url", "reportpoi", "user", "value", "created")

    def create(self, validated_data):

        with transaction.atomic():

            instance = Contribution.objects.create(**validated_data)
            reportpoid = instance.reportpoi
            reportpoid.modified = instance.created
            reportpoid.save()

        return reportpoid.status
