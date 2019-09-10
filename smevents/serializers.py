from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("pk", "application", "e_type", "agent", "position", "instant", "extra_information")
