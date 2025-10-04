from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'plate_number',
            'vin',
            'brand',
            'model',
            'year',
            'status',
            'mileage',
            'is_collector',
            'hitched_to',
            'last_service_at',
            'payload_capacity_kg',
        ]
        widgets = {
            'plate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_collector': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'last_service_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payload_capacity_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'hitched_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Динамически настраиваем выбор для hitched_to
        if self.instance and self.instance.is_collector:
            # Для прицепа показываем только автомобили
            self.fields['hitched_to'].queryset = Vehicle.objects.filter(is_collector=False)
            self.fields['hitched_to'].label = "Автомобиль для привязки"
        else:
            # Для автомобилей скрываем это поле
            self.fields['hitched_to'].widget = forms.HiddenInput()
            self.fields['hitched_to'].required = False