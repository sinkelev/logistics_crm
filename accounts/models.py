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
    phone = models.CharField("Телефон основной", max_length=20, blank=True)
    phone_work = models.CharField("Телефон рабочий", max_length=20, blank=True)
    patronymic = models.CharField("Отчество", max_length=150, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    passport_number = models.CharField("Паспорт (серия и номер)", max_length=20, blank=True)
    passport_issued_by = models.CharField("Кем выдан паспорт", max_length=255, blank=True)
    passport_issued_at = models.DateField("Дата выдачи паспорта", null=True, blank=True)
    snils = models.CharField("СНИЛС", max_length=20, blank=True)
    inn = models.CharField("ИНН", max_length=20, blank=True)
    hired_at = models.DateField("Дата трудоустройства", null=True, blank=True)
    fired_at = models.DateField("Дата увольнения", null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''} ({self.get_role_display()})"