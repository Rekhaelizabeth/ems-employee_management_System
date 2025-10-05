from rest_framework import serializers
from .models import Employee, EmployeeFieldValue
from forms_app.models import FormField, FormTemplate

class EmployeeValueSerializer(serializers.ModelSerializer):
    field_label = serializers.CharField(source="field.label", read_only=True)
    field_type = serializers.CharField(source="field.field_type", read_only=True)

    class Meta:
        model = EmployeeFieldValue
        fields = ["field", "field_label", "field_type", "value"]

class EmployeeSerializer(serializers.ModelSerializer):
    values = EmployeeValueSerializer(many=True)
    template_name = serializers.CharField(source="template.name", read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "template", "template_name", "created_at", "updated_at", "values"]

    def validate(self, attrs):
        template = attrs.get("template") or getattr(self.instance, "template", None)
        if not template:
            raise serializers.ValidationError("template is required")
        return attrs

    def create(self, validated_data):
        values_data = validated_data.pop("values", [])
        employee = Employee.objects.create(**validated_data)
        # enforce matching fields from template
        field_ids = set(template_field.id for template_field in validated_data["template"].fields.all())
        for v in values_data:
            field = v["field"]
            if field.id not in field_ids:
                raise serializers.ValidationError("Field not in template")
            EmployeeFieldValue.objects.create(employee=employee, field=field, value=v.get("value", ""))
        return employee

    def update(self, instance, validated_data):
        values_data = self.initial_data.get("values", [])
        instance.save()
        # upsert values
        for v in values_data:
            field_id = v["field"]
            val = v.get("value", "")
            efv, _ = EmployeeFieldValue.objects.get_or_create(employee=instance, field_id=field_id)
            efv.value = val
            efv.save()
        return instance
