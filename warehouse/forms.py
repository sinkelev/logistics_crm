from django import forms
from .models import Order
from django.contrib.auth import get_user_model
from vehicles.models import Vehicle
from .services import check_delivery_status

User = get_user_model()


class DatalistInput(forms.TextInput):
    """Кастомный input с поддержкой HTML5 <datalist>"""
    template_name = 'warehouse/widgets/datalist.html'

    def __init__(self, attrs=None, datalist=None):
        self.datalist = datalist or []
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['datalist'] = self.datalist
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
            'vat_status': forms.Select(attrs={'class': 'form-control'}),
            'is_return_trip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер счета'}),
            'act_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер акта выполненных работ'}),
            'invoice_act_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер счет-фактуры'}),
            'date_order': forms.DateInput(attrs={'type': 'date'}),
            'date_invoice': forms.DateInput(attrs={'type': 'date'}),
            'date_act': forms.DateInput(attrs={'type': 'date'}),
            'date_invoice_act': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        initial_invoice_number = kwargs.pop('initial_invoice_number', None)
        super().__init__(*args, **kwargs)

        if initial_invoice_number:
            self.fields['invoice_number'].initial = initial_invoice_number

        # Загружаем варианты для datalist динамически здесь, а не в Meta (чтобы не рушить миграции)
        try:
            drivers = User.objects.filter(role='driver').order_by('last_name')
            driver_names = []
            for d in drivers:
                if hasattr(d, 'get_full_name_with_middle'):
                    driver_names.append(d.get_full_name_with_middle())
                else:
                    driver_names.append(d.get_full_name() or d.username)

            self.fields['document_driver'].widget = DatalistInput(
                attrs={'class': 'form-control', 'placeholder': 'Выберите или введите ФИО'},
                datalist=driver_names
            )

            vehicles = Vehicle.objects.all()
            self.fields['document_vehicle'].widget = DatalistInput(
                attrs={'class': 'form-control', 'placeholder': 'Выберите или введите гос. номер'},
                datalist=[str(v) for v in vehicles]
            )
        except Exception:
            # если база недоступна (например, миграции) — используем обычные TextInput
            self.fields['document_driver'].widget = forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите ФИО водителя'}
            )
            self.fields['document_vehicle'].widget = forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите гос. номер'}
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Проверяем доставку при изменении номера РПО
        if (instance.rpo_number and
                instance.rpo_number != self.initial.get('rpo_number')):

            delivery_date = check_delivery_status(instance.rpo_number)
            if delivery_date:
                instance.delivery_date = delivery_date

        if commit:
            instance.save()
        return instance