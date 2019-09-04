from django.db import transaction
from rest_framework import serializers

from .models import TimeRecord


class TimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRecord
        fields = ("user", "spot", "time_taked", "created", "from_app", "action")

    def create(self, validated_data):
        with transaction.atomic():
            instance = TimeRecord.objects.create(**validated_data)

        instance = TimeRecord.objects.get(pk=instance.pk)
        return instance
