# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

EXTRA_TYPE_CHOICES = [
    ("text", "Text"),
    ("number", "Number"),
    ("date", "Date"),
    ("email", "Email"),
    ("password", "Password"),
]

class UserExtraField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="extra_fields")
    label = models.CharField(max_length=120)
    type  = models.CharField(max_length=20, choices=EXTRA_TYPE_CHOICES, default="text")
    value = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # (Optional) avoid duplicate labels for the same user
        constraints = [
            models.UniqueConstraint(fields=["user", "label"], name="uniq_user_label")
        ]

    def __str__(self):
        return f"{self.user.username} · {self.label} = {self.value}"