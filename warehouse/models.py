from django.db import models
from django.utils import timezone


class Cargo(models.Model):
    VAT_STATUS = [
        ("with_vat", "С НДС"),
        ("without_vat", "Без НДС"),
    ]

    code = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    volume_m3 = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    shipper = models.CharField(max_length=255)
    consignee = models.CharField(max_length=255)
    vat_status = models.CharField(
        max_length=15,
        choices=VAT_STATUS,
        default="with_vat",
    )
    is_return_trip = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code}: {self.description[:30]}"


class WarehouseEntry(models.Model):
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
        related_name="warehouse_entries",
    )
    arrived_at = models.DateTimeField()
    released_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    @property
    def storage_time_hours(self):
        end_time = self.released_at or timezone.now()
        return (end_time - self.arrived_at).total_seconds() / 3600

    def __str__(self):
        status = "на складе" if not self.released_at else "выдан"
        return f"{self.cargo.code} — {status}"