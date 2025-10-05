from django.shortcuts import render

from rest_framework import generics, permissions, serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from accounts.serializers import RegisterSerializer 
from .serializers import ProfileFlatSerializer, AdminUserRowSerializer

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

class AdminUserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]  # only staff/superuser
    serializer_class = AdminUserRowSerializer
    queryset = User.objects.all().prefetch_related("extra_fields")  # optimize queries

class AdminUserDetailView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        target = self.get_object()
        if target.is_superuser:
            return Response({"detail": "Cannot delete a superuser."}, status=status.HTTP_403_FORBIDDEN)
        if target == request.user:
            return Response({"detail": "You cannot delete your own account."}, status=status.HTTP_400_BAD_REQUEST)
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)