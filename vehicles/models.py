from django.db import models
from django.core.exceptions import ValidationError


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ("active", "В эксплуатации"),
        ("maintenance", "На обслуживании"),
        ("inactive", "Неактивен"),
    ]

    plate_number = models.CharField(max_length=20, unique=True, verbose_name="Гос. номер")
    vin = models.CharField(max_length=17, blank=True, verbose_name="VIN-код")
    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, blank=True, verbose_name="Модель")
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Год выпуска")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="Статус",
    )
    mileage = models.PositiveIntegerField(default=0, verbose_name="Пробег (км)")
    is_collector = models.BooleanField(default=False, verbose_name="Полуприцеп/Прицеп")
    last_service_at = models.DateField(null=True, blank=True, verbose_name="Дата последнего ТО")
    payload_capacity_kg = models.PositiveIntegerField(null=True, blank=True, verbose_name="Грузоподъёмность (кг)")
    hitched_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trailers',
        limit_choices_to={'is_collector': False},
        verbose_name="Привязан к автомобилю"
    )

    def clean(self):
        if self.hitched_to and self.id == self.hitched_to.id:
            raise ValidationError("Транспорт не может быть привязан к самому себе.")
        if self.is_collector and self.hitched_to and self.hitched_to.is_collector:
            raise ValidationError("Прицеп не может быть привязан к другому прицепу.")

    def __str__(self):
        return f"{self.plate_number} — {self.brand} {self.model}".strip()

    class Meta:
        ordering = ["plate_number"]
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"