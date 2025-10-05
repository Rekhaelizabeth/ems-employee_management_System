# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # expect a list of {label, type, value} objects; optional
    extra_fields = serializers.ListField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "extra_fields"]

    def create(self, validated_data):
        extra_fields = validated_data.pop("extra_fields", [])
        print("extrafields",extra_fields)
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        # create profile and save extras
        Profile.objects.create(user=user, extras=extra_fields)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    # include extras from related profile
    extras = serializers.JSONField(source="profile.extras", required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "extras"]

    def update(self, instance, validated_data):
        # pull nested profile.extras if provided
        profile_data = validated_data.pop("profile", {})
        extras = profile_data.get("extras", None)

        # update user basics
        for attr in ["first_name", "last_name", "email"]:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.save()

        # ensure profile exists, then update extras if provided
        profile, _ = Profile.objects.get_or_create(user=instance)
        if extras is not None:
            profile.extras = extras
            profile.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        validate_password(value)
        return value
