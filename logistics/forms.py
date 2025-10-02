from django import forms
from django.db import transaction
from .models import Route, RouteCargo
from warehouse.models import Order


class RouteForm(forms.ModelForm):
    cargoes = forms.ModelMultipleChoiceField(
        queryset=Order.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Заявки для добавления в рейс",
    )

    class Meta:
        model = Route
        fields = [
            "route_number", "vehicle", "driver", "legal_entity", "date_start",
            "planned_end", "cargoes", "notes",
        ]
        widgets = {
            "route_number": forms.TextInput(attrs={'placeholder': 'Оставьте пустым для авто-генерации'}),
            "date_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "planned_end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {
            "route_number": "Номер маршрута", "vehicle": "Автомобиль", "driver": "Водитель",
            "legal_entity": "Юрлицо", "date_start": "Дата загрузки",
            "planned_end": "Плановое завершение", "notes": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route_number'].required = False
        if self.instance and self.instance.pk:
            self.fields['cargoes'].queryset = Order.objects.filter(
                routecargo__isnull=True) | self.instance.cargoes.all()
            self.fields['cargoes'].initial = self.instance.cargoes.all()
        else:
            self.fields['cargoes'].queryset = Order.objects.filter(routecargo__isnull=True)

    def save(self, commit=True):
        route_instance = super().save(commit=False)

        if not route_instance.pk and not route_instance.route_number:
            date_start = self.cleaned_data.get('date_start')
            driver = self.cleaned_data.get('driver')
            vehicle = self.cleaned_data.get('vehicle')

            parts = []
            if date_start: parts.append(date_start.strftime('%d.%m.%y'))
            if driver and driver.last_name: parts.append(driver.last_name.strip().upper())
            if vehicle:
                plate = ''.join(filter(str.isalnum, vehicle.plate_number)).upper()
                parts.append(plate)

            if len(parts) == 3:
                route_instance.route_number = "-".join(parts)

        if commit:
            route_instance.save()

            cargoes = self.cleaned_data.get('cargoes', [])

            with transaction.atomic():
                route_instance.routecargo_set.all().delete()

                new_cargo_links = []
                for position, cargo in enumerate(cargoes, start=1):
                    new_cargo_links.append(
                        RouteCargo(route=route_instance, cargo=cargo, position=position)
                    )
                if new_cargo_links:
                    RouteCargo.objects.bulk_create(new_cargo_links)

        return route_instance
