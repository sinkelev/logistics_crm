from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("driver", "Водитель"),
        ("logist", "Логист"),
        ("warehouse", "Кладовщик"),
        ("finance", "Бухгалтер"),
        ("manager", "Руководитель"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    hired_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"