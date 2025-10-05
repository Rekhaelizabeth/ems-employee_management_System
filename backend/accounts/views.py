from django.shortcuts import render

from rest_framework import generics, permissions, serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from accounts.serializers import RegisterSerializer 
from .serializers import ProfileFlatSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileFlatSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    def validate_new_password(self, value):
        validate_password(value)
        return value

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):  # dummy
        return self.request.user
    def update(self, request, *args, **kwargs):
        user = request.user
        s = self.get_serializer(data=request.data); s.is_valid(raise_exception=True)
        if not user.check_password(s.validated_data["old_password"]):
            raise serializers.ValidationError({"old_password": "Wrong password"})
        user.set_password(s.validated_data["new_password"]); user.save()
        return Response({"detail": "Password changed"})

