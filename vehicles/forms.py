from django import forms
from .models import Vehicle


class TrailerForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'plate_number',
            'vin',
            'brand',
            'model',
            'year',
            'status',
            'hitched_to', # Поле для привязки к автомобилю
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
            'last_service_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payload_capacity_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'hitched_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hitched_to'].queryset = Vehicle.objects.filter(is_collector=False)
        self.fields['hitched_to'].label = "Привязать к автомобилю"

    def save(self, commit=True):
        # Принудительно устанавливаем, что это полуприцеп
        self.instance.is_collector = True
        return super().save(commit)


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
        }

    def save(self, commit=True):
        # Убедимся, что при сохранении is_collector=False
        self.instance.is_collector = False
        return super().save(commit)