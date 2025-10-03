from django import forms
from .models import User


class DriverForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "last_name",
            "first_name",
            "patronymic",           # отчество
            "birth_date",
            "phone",
            "phone_work",
            "email",
            "passport_number",      # здесь и серия, и номер
            "passport_issued_by",
            "passport_issued_at",
            "snils",
            "inn",
            "hired_at",
            "fired_at",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "passport_issued_at": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hired_at": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fired_at": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "patronymic": "Отчество",
            "birth_date": "Дата рождения",
            "phone": "Основной телефон",
            "phone_work": "Рабочий телефон",
            "passport_number": "Паспорт (серия и номер)",
            "passport_issued_by": "Кем выдан паспорт",
            "passport_issued_at": "Дата выдачи паспорта",
            "snils": "СНИЛС",
            "inn": "ИНН",
            "hired_at": "Дата трудоустройства",
            "fired_at": "Дата увольнения",
            "email": "Электронная почта",
        }

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.role = "driver"
        if not driver.pk:  # при создании нового
            driver.set_password(User.objects.make_random_password())  # генерим временный пароль
        if commit:
            driver.save()
        return driver