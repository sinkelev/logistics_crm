from django.db import models
from django.utils import timezone
from django.conf import settings
from vehicles.models import Vehicle

class Order(models.Model):
    VAT_STATUS = [
        ("with_vat", "С НДС"),
        ("without_vat", "Без НДС"),
    ]

    code = models.CharField(max_length=30, unique=True, verbose_name="Складской номер")
    order_number=models.CharField(max_length=30, blank=True, verbose_name="Номер заявки")
    description = models.TextField(verbose_name="Описание")
    places = models.PositiveIntegerField(default=1, verbose_name="Места (шт)")
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Вес (кг)")
    volume_m3 = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Объем (м³)",
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Ставка"
    )
    customer = models.CharField(max_length=255, verbose_name="Заказчик")
    vat_status = models.CharField(
        max_length=15,
        choices=VAT_STATUS,
        default="with_vat",
        verbose_name="Статус НДС",
    )
    is_return_trip = models.BooleanField(default=False, verbose_name="Обратный рейс")
    invoice_number = models.CharField(max_length=50, blank=True, verbose_name="Номер счета")
    act_number = models.CharField(max_length=50, blank=True, verbose_name="Номер акта")
    invoice_act_number = models.CharField(max_length=50, blank=True, verbose_name="Номер счет-фактуры")
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "driver"},
        verbose_name="Водитель",
        related_name="assigned_orders"
    )
    document_driver = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Водитель по документам"
    )
    route_from = models.CharField(max_length=255, verbose_name="Маршрут От")
    route_to = models.CharField(max_length=255, verbose_name="Маршрут До")
    date_order = models.DateField(
        verbose_name="Дата заявки",
        default=timezone.now
    )
    date_invoice = models.DateField(
        verbose_name="Дата счёта",
        blank=True,
        null=True
    )
    date_act = models.DateField(
        verbose_name="Дата акта",
        blank=True,
        null=True
    )
    date_invoice_act = models.DateField(
        verbose_name="Дата счет-фактуры",
        blank=True,
        null=True
    )
    RPO_STATUS_CHOICES = [
        ('not_sent', 'Не отправлено'),
        ('created', 'Создано'),
        ('sent', 'Отправлено'),
        ('delivered', 'Доставлено'),
        ('problem', 'Проблема'),
    ]
    rpo_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер РПО"
    )
    rpo_status = models.CharField(
        max_length=20,
        choices=RPO_STATUS_CHOICES,
        default='not_sent',
        verbose_name="Статус РПО"
    )
    actual_vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Машина по факту",
        related_name="assigned_orders"
    )
    document_vehicle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Машина по документам"
    )

    def save(self, *args, **kwargs):
        # Автоматическая установка даты счёта
        if not self.date_invoice and self.date_order:
            self.date_invoice = self.date_order

        # Автоматическая установка даты счет-фактуры
        if self.date_act and not self.date_invoice_act:
            self.date_invoice_act = self.date_act

        # Автоматически устанавливаем документального водителя только при создании
        if not self.pk and not self.document_driver and self.driver:
            self.document_driver = self.driver.get_full_name() or self.driver.username

        # Для существующих записей запрещаем автоматическое изменение
        if not self.pk and not self.document_vehicle and self.actual_vehicle:
            self.document_vehicle = str(self.actual_vehicle)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code}: {self.description[:30]}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class WarehouseEntry(models.Model):
    cargo = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="warehouse_entries",
        verbose_name="Заявка",
    )
    arrived_at = models.DateTimeField(verbose_name="Дата прибытия")
    released_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата выдачи")
    location = models.CharField(max_length=100, verbose_name="Местоположение")
    notes = models.TextField(blank=True, verbose_name="Заметки")

    @property
    def storage_time_hours(self):
        end_time = self.released_at or timezone.now()
        return (end_time - self.arrived_at).total_seconds() / 3600

    def __str__(self):
        status = "на складе" if not self.released_at else "выдан"
        return f"Складская запись для {self.cargo.code} — {status}"

    class Meta:
        verbose_name = "Складская запись"
        verbose_name_plural = "Складские записи"