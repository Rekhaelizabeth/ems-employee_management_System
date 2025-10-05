from django.db import models
from django.contrib.auth import get_user_model
from forms_app.models import FormTemplate, FormField

User = get_user_model()

class Employee(models.Model):
    template = models.ForeignKey(FormTemplate, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmployeeFieldValue(models.Model):
    employee = models.ForeignKey(Employee, related_name="values", on_delete=models.CASCADE)
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.TextField(blank=True)

    class Meta:
        unique_together = ("employee", "field")
