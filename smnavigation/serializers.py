from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import NavigationRequest


class NavigationRequestSerializer(serializers.ModelSerializer):
    # state = serializers.SerializerMethodField()

    class Meta:
        model = NavigationRequest
        fields = (
            "url",
            "user_requested",
            "finished",
            "origin",
            "destination",
            "score",
            "route",
            "report_severe",
            "report_light",
        )

    def update(self, instance, validated_data):

        with transaction.atomic():
            instance.score = validated_data.get("score")
            instance.finished = validated_data.get("finished")
            instance.finish_time = timezone.now()
            instance.save()

        return instance
