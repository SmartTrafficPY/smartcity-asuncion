from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from .models import UcarpoolingProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UcarpoolingProfile
        fields = ("sex", "smoker", "musicTaste", "eloquenceLevel")


class UserSerializer(serializers.ModelSerializer):
    # TODO CHANGE SERIALIZERS
    ucarpoolingprofile = ProfileSerializer(required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Leave empty if no change needed",
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = ("url", "email", "password", "first_name", "last_name", "ucarpoolingprofile")

    def create(self, validated_data):
        profile_data = validated_data.pop("ucarpoolingprofile", None)

        validated_data["username"] = validated_data["email"]

        password = validated_data.get("password")
        if password:
            validated_data["password"] = make_password(password)

        with transaction.atomic():
            instance = User.objects.create(**validated_data)
            if profile_data:
                UcarpoolingProfile.objects.create(user=instance, **profile_data)

        instance = User.objects.get(pk=instance.pk)
        return instance

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("ucarpoolingprofile", None)

        password = validated_data.get("password")
        if password:
            instance.password = make_password(password)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("email", instance.username)

        with transaction.atomic():
            instance.save()

            if profile_data:
                profile = instance.ucarpoolingprofile
                if profile:
                    profile.smoker = profile_data.get("smoker", profile.smoker)
                    profile.sex = profile_data.get("sex", profile.sex)
                    profile.musicTaste = profile_data.get("musicTaste", profile.musicTaste)
                    profile.save()

                else:
                    UcarpoolingProfile.objects.create(user=instance, **profile_data)

        instance = User.objects.get(pk=instance.pk)
        return instance
