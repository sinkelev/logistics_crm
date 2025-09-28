from django.db import models


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ("active", "В эксплуатации"),
        ("maintenance", "На обслуживании"),
        ("inactive", "Неактивен"),
    ]

    plate_number = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=17, blank=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )
    mileage = models.PositiveIntegerField(default=0)
    fuel_type = models.CharField(max_length=20, default="diesel")
    is_collector = models.BooleanField(default=False)
    last_service_at = models.DateField(null=True, blank=True)
    payload_capacity_kg = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.plate_number} — {self.brand} {self.model}".strip()

    class Meta:
        ordering = ["plate_number"]