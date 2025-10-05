from rest_framework import serializers
from .models import FormTemplate, FormField

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ["id", "label", "field_type", "required", "order", "options_json", "template"]
        read_only_fields = ["template"]

class FormTemplateSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)

    class Meta:
        model = FormTemplate
        fields = ["id", "name", "description", "fields", "created_at", "updated_at"]

    def create(self, validated_data):
        fields_data = validated_data.pop("fields", [])
        template = FormTemplate.objects.create(**validated_data)
        for idx, f in enumerate(fields_data):
            FormField.objects.create(template=template, order=f.get("order", idx), **f)
        return template

    def update(self, instance, validated_data):
        fields_data = validated_data.pop("fields", [])
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        # simple replace approach: delete then recreate (fast for test)
        instance.fields.all().delete()
        for idx, f in enumerate(fields_data):
            FormField.objects.create(template=instance, order=f.get("order", idx), **f)
        return instance
