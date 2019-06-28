from rest_framework import serializers

from .models import Sp_profiles

# https://docs.djangoproject.com/en/2.2/topics/serialization/


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sp_profiles
        fields = "__all__"
