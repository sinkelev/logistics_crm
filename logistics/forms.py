from django import forms
from .models import Route, RouteCargo
from warehouse.models import Order

class RouteForm(forms.ModelForm):
    cargoes = forms.ModelMultipleChoiceField(
        queryset=Order.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Заявки для маршрута",
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

        def save(self, commit=True):
            cargoes = list(self.cleaned_data.get("cargoes") or [])
            with transaction.atomic():
                route = super().save(commit=commit)
                if commit:
                    self._update_cargo_relations(route, cargoes)
                else:
                    self._pending_cargoes = cargoes
            return route

        def save_m2m(self):
            super().save_m2m()
            pending = getattr(self, "_pending_cargoes", None)
            if pending is not None:
                self._update_cargo_relations(self.instance, pending)
                delattr(self, "_pending_cargoes")

        def _update_cargo_relations(self, route, cargoes):
            RouteCargo.objects.filter(route=route).delete()
            for position, cargo in enumerate(cargoes, start=1):
                RouteCargo.objects.create(
                    route=route,
                    cargo=cargo,
                    position=position,
                )
            if route.driver and cargoes:
                Order.objects.filter(pk__in=[cargo.pk for cargo in cargoes]).update(driver=route.driver)