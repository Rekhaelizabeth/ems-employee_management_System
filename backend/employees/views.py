from django.shortcuts import render

from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Employee, EmployeeFieldValue
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().select_related("template").prefetch_related("values__field")
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    # dynamic search by label=value: ?name=John&JoiningDate=2024-01-01
    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        # collect all label filters
        filters = []
        for key, value in params.items():
            if key in ["page", "page_size"]:  # ignore pagination keys
                continue
            if value.strip() == "":
                continue
            filters.append(Q(values__field__label__iexact=key) & Q(values__value__icontains=value))
        if filters:
            q = Q()
            for f in filters:
                q &= f
            qs = qs.filter(q).distinct()
        return qs

