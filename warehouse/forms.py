from django import forms
from .models import Order
from django.contrib.auth import get_user_model
from vehicles.models import Vehicle

User = get_user_model()

class DatalistInput(forms.TextInput):
    template_name = 'warehouse/widgets/datalist.html'

    def __init__(self, attrs=None, datalist=None):
        self.datalist = datalist or []
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['datalist'] = self.datalist
        # Добавляем ID для datalist, чтобы связать его с input
        context['widget']['attrs']['list'] = f'datalist_{name}'
        return context

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
            'order_number',
            'description',
            'places',
            'weight_kg',
            'volume_m3',
            'rate',
            'customer',
            'route_from',
            'route_to',
            'vat_status',
            'is_return_trip',
            'invoice_number',
            'act_number',
            'invoice_act_number',
            'driver',
            'actual_vehicle',
            'document_driver',
            'document_vehicle',
            'date_order',
            'date_invoice',
            'date_act',
            'date_invoice_act',
            'rpo_number',
            'rpo_status',
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Уникальный складской номер'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Уникальный код заявки'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Подробное описание груза'}),
            'places': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество мест'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Вес в кг'}),
            'volume_m3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Объем в м³'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ставка за перевозку'}),
            'customer': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Имя заказчика или название компании'}),
            'route_from': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пункт отправления'}),
            'route_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пункт назначения'}),
            'document_driver': DatalistInput(
                attrs={'class': 'form-control', 'placeholder': 'Выберите или введите ФИО'},
                # Получаем список ФИО всех водителей
                datalist=[u.get_full_name() or u.username for u in User.objects.filter(role='driver').order_by('last_name')]
            ),
            'document_vehicle': DatalistInput(
                attrs={'class': 'form-control', 'placeholder': 'Выберите или введите гос. номер'},
                datalist=[str(v) for v in Vehicle.objects.all()]
            ),
            'vat_status': forms.Select(attrs={'class': 'form-control'}),
            'is_return_trip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер счета'}),
            'act_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Номер акта выполненных работ'}),
            'invoice_act_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер счет-фактуры'}),
            'date_order': forms.DateInput(attrs={'type': 'date'}),
            'date_invoice': forms.DateInput(attrs={'type': 'date'}),
            'date_act': forms.DateInput(attrs={'type': 'date'}),
            'date_invoice_act': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        initial_invoice_number = kwargs.pop('initial_invoice_number', None)
        super().__init__(*args, **kwargs)

        # Если передано начальное значение, устанавливаем его для поля
        if initial_invoice_number:
            self.fields['invoice_number'].initial = initial_invoice_number
            # Делаем поле "Машина по факту" только для чтения
        #self.fields['actual_vehicle'].widget.attrs['disabled'] = True