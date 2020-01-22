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
