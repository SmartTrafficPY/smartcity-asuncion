from django.db import transaction
from rest_framework import serializers

from .models import Report, StatusUpdate


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("url", "user_created", "report_type", "modified", "status", "coordinates")

    def create(self, validated_data):

        with transaction.atomic():

            instance = Report.objects.create(**validated_data)

        instance = Report.objects.get(pk=instance.pk)
        return instance


class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdate
        fields = ("url", "reportid", "user", "value", "created")

    def create(self, validated_data):

        with transaction.atomic():

            instance = StatusUpdate.objects.create(**validated_data)
            reportpoid = instance.reportid
            reportpoid.modified = instance.created
            reportpoid.save()

        return instance
