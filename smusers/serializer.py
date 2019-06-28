from rest_framework import serializers

from .models import User


class userSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
