from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from .models import SmartParkingProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartParkingProfile
        fields = ("birth_date", "sex")


class UserSerializer(serializers.ModelSerializer):
    smartparkingprofile = ProfileSerializer(required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Leave empty if no change needed",
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        # fields = "__all__"
        fields = ("id", "password", "username", "first_name", "last_name", "email", "smartparkingprofile")

    def create(self, validated_data):
        profile_data = validated_data.pop("smartparkingprofile", None)

        password = validated_data.get("password")
        if password:
            validated_data["password"] = make_password(password)

        with transaction.atomic():
            instance = User.objects.create(**validated_data)
            if profile_data:
                SmartParkingProfile.objects.create(user=instance, **profile_data)

        instance = User.objects.get(pk=instance.pk)
        return instance

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("smartparkingprofile", None)

        password = validated_data.get("password")
        if password:
            instance.password = make_password(password)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        with transaction.atomic():
            instance.save()

            if profile_data:
                profile = instance.smartparkingprofile
                if profile:
                    profile.birth_date = profile_data.get("birth_date", profile.birth_date)
                    profile.sex = profile_data.get("sex", profile.sex)
                    profile.save()
                else:
                    SmartParkingProfile.objects.create(user=instance, **profile_data)

        instance = User.objects.get(pk=instance.pk)
        return instance
