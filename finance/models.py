from django.conf import settings
from django.db import models


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("fuel", "ГСМ"),
        ("maintenance", "Ремонт и ТО"),
        ("salary", "Заработная плата"),
        ("warehouse", "Складские расходы"),
        ("other", "Прочее"),
    ]

    route = models.ForeignKey(
        "logistics.Route",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )
    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    incurred_at = models.DateField()
    description = models.TextField(blank=True)
    document = models.FileField(upload_to="expenses/%Y/%m/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        parts = [self.get_category_display(), f"{self.amount}"]
        if self.route:
            parts.append(f"маршрут {self.route.route_number}")
        return " — ".join(parts)


class FuelTransaction(models.Model):
    route = models.ForeignKey(
        "logistics.Route",
        on_delete=models.CASCADE,
        related_name="fuel_transactions",
    )
    liters = models.DecimalField(max_digits=7, decimal_places=2)
    price_per_liter = models.DecimalField(max_digits=7, decimal_places=2)
    purchased_at = models.DateTimeField()
    fuel_card_number = models.CharField(max_length=30, blank=True)
    receipt_photo = models.FileField(upload_to="fuel_receipts/%Y/%m/", blank=True)

    def __str__(self):
        return f"ГСМ {self.route.route_number}: {self.liters} л"

    @property
    def total_cost(self):
        return self.liters * self.price_per_liter


class PayrollRecord(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payroll_records",
    )
    period_start = models.DateField()
    period_end = models.DateField()
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    route = models.ForeignKey(
        "logistics.Route",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payroll_records",
    )
    comment = models.TextField(blank=True)
    paid_at = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} — {self.period_start:%d.%m.%Y}–{self.period_end:%d.%m.%Y}"