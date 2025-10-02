from django.conf import settings
from django.db import models


class Route(models.Model):
    LEGAL_ENTITY_CHOICES = [
        ("llc", "ООО (с НДС)"),
        ("sole", "ИП (без НДС)"),
    ]

    route_number = models.CharField(max_length=30, unique=True)
    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        related_name="routes",
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "driver"},
    )
    date_start = models.DateTimeField()
    planned_end = models.DateTimeField(null=True, blank=True)
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    legal_entity = models.CharField(
        max_length=10,
        choices=LEGAL_ENTITY_CHOICES,
        default="llc",
    )
    distance_km = models.DecimalField(
        max_digits=7,
        decimal_places=1,
        null=True,
        blank=True,
    )
    notes = models.TextField(blank=True)

    cargoes = models.ManyToManyField(
        "warehouse.Order",
        through="RouteCargo",
    )

    def __str__(self):
        return self.route_number


class RouteCargo(models.Model):
    route = models.ForeignKey(
        "logistics.Route",
        on_delete=models.CASCADE,
    )
    cargo = models.ForeignKey(
        "warehouse.Order",
        on_delete=models.CASCADE,
    )
    position = models.PositiveIntegerField(default=1)
    is_collected_by_collector = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.route} — {self.cargo} (#{self.position})"
