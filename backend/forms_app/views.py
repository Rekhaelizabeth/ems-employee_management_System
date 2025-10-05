from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import FormTemplate, FormField
from .serializers import FormTemplateSerializer, FormFieldSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: return True
        return getattr(obj, "created_by_id", None) == request.user.id

class FormTemplateViewSet(viewsets.ModelViewSet):
    queryset = FormTemplate.objects.all().prefetch_related("fields")
    serializer_class = FormTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class FormFieldViewSet(viewsets.ModelViewSet):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

