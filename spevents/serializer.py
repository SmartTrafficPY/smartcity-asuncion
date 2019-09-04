from django.db import transaction
from rest_framework import serializers

from .models import Events


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ("user", "spot", "lot", "created", "action")

    def create(self, validated_data):
        with transaction.atomic():
            instance = Events.objects.create(**validated_data)

        instance = Events.objects.get(pk=instance.pk)
        return instance
