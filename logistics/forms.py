from django import forms
from .models import Route
from warehouse.models import Cargo

class RouteForm(forms.ModelForm):
    cargoes = forms.ModelMultipleChoiceField(
        queryset=Cargo.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Грузы для маршрута",
    )

    class Meta:
        model = Route
        fields = [
            "route_number",
            "vehicle",
            "driver",
            "legal_entity",
            "planned_start",
            "planned_end",
            "cargoes",
            "notes",
        ]
        widgets = {
            "planned_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "planned_end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {
            "route_number": "Номер маршрута",
            "vehicle": "Автомобиль",
            "driver": "Водитель",
            "legal_entity": "Юрлицо",
            "planned_start": "Плановое начало",
            "planned_end": "Плановое завершение",
            "notes": "Комментарий",
        }