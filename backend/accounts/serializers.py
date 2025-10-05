# accounts/serializers.py
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserExtraField

class ExtraFieldItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtraField
        fields = ["label", "type", "value"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    extra_fields = ExtraFieldItemSerializer(many=True, required=False, write_only=True)
    extras = ExtraFieldItemSerializer(source="extra_fields", many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "extra_fields", "extras"]

    @transaction.atomic
    def create(self, validated_data):
        extra_items = validated_data.pop("extra_fields", [])
        print("DEBUG: validated extra_items =", extra_items)  # <— TEMP LOG
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        if extra_items:
            rows = [UserExtraField(user=user, **item) for item in extra_items]
            UserExtraField.objects.bulk_create(rows)
            print("DEBUG: created extras =", len(rows))       # <— TEMP LOG
        else:
            print("DEBUG: no extras provided")                # <— TEMP LOG
        return user
    
class ExtraFieldReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtraField
        fields = ["label", "value"] 

class ProfileFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]

    def to_representation(self, obj):
        data = super().to_representation(obj) 
        extras_map = {ef.label: ef.value for ef in obj.extra_fields.all()}
        data.update(extras_map)
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        validate_password(value)
        return value

class AdminUserRowSerializer(serializers.ModelSerializer):
    # return extras as a dict: {"Department": "R&D", "Role": "Manager"}
    extras = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_superuser", "is_staff", "extras"]

    def get_extras(self, obj):
        # obj.extra_fields is from related_name="extra_fields" on your FK
        return {ef.label: ef.value for ef in obj.extra_fields.all()}