from django import forms
from .models import Order
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderForm(forms.ModelForm):
    driver = forms.ModelChoiceField(
        queryset=User.objects.filter(role='driver'),
        required=False,
        label="Водитель",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = [
            'code',
            'description',
            'weight_kg',
            'volume_m3',
            'customer',
            'consignee',
            'vat_status',
            'is_return_trip',
            'invoice_number',
            'act_number',
            'invoice_act_number',
            'driver',
            'document_driver',
            'route_from',
            'route_to',
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Уникальный код заказа'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Подробное описание груза'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Вес в кг'}),
            'volume_m3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Объем в м³'}),
            'customer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя заказчика или название компании'}),
            'consignee': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя получателя или название компании'}),
            'vat_status': forms.Select(attrs={'class': 'form-control'}),
            'is_return_trip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер счета'}),
            'act_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер акта выполненных работ'}),
            'invoice_act_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер счет-фактуры'}),
            'document_driver': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ФИО водителя по документам'}),
            'route_from': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пункт отправления'}),
            'route_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пункт назначения'}),
        }