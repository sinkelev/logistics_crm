import re
import json

from urllib.parse import urlencode
from vehicles.models import Vehicle
from django.db import models
from django.db.models.functions import Length, Right, Cast
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    UpdateView,
)

from logistics.models import Route
from logistics.forms import RouteForm
from accounts.models import User
from accounts.forms import DriverForm
from warehouse.models import Order
from warehouse.forms import OrderForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_routes"] = Route.objects.select_related("vehicle", "driver").order_by("-date_start")[:5]
        context["drivers_count"] = User.objects.filter(role="driver").count()
        # Можно добавить статистику по заявкам, если нужно
        # context["orders_count"] = Order.objects.count()
        return context

class RouteContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Готовим данные о водителях: { "id": "ФАМИЛИЯ", ... }
        drivers = User.objects.filter(role="driver")
        drivers_map = {
            str(driver.id): driver.last_name.strip().upper()
            for driver in drivers if driver.last_name
        }

        vehicles = Vehicle.objects.all()
        vehicles_map = {
            str(vehicle.id): ''.join(filter(str.isalnum, vehicle.plate_number)).upper()
            for vehicle in vehicles
        }

        context['drivers_map_json'] = json.dumps(drivers_map)
        context['vehicles_map_json'] = json.dumps(vehicles_map)

        return context


class RouteCreateView(LoginRequiredMixin, RouteContextMixin, CreateView):
    template_name = "frontend/route_form.html"
    form_class = RouteForm

    def get_success_url(self):
        return reverse("frontend:route_detail", kwargs={"pk": self.object.pk})

class DriverCreateView(LoginRequiredMixin, CreateView):
    template_name = "frontend/driver_form.html"
    form_class = DriverForm
    success_url = reverse_lazy("frontend:dashboard")


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order # Указываем модель, для которой создаем объект
    template_name = "frontend/order_form.html"
    form_class = OrderForm # Используем нашу OrderForm

    def get_success_url(self):
        return reverse("frontend:order_detail", kwargs={"pk": self.object.pk})

    def get_next_invoice_number(self):
        """
        Находит последний номер счета и возвращает следующий по порядку.
        """
        # Ищем последнюю заявку с непустым номером счета, сортируя по ID
        last_order_with_invoice = Order.objects.filter(
            invoice_number__isnull=False
        ).exclude(
            invoice_number__exact=''
        ).order_by('-id').first()

        if not last_order_with_invoice:
            return "1"  # Если счетов нет вообще, начинаем с "1"

        last_invoice_number = last_order_with_invoice.invoice_number

        # Используем регулярное выражение для поиска чисел в конце строки
        match = re.search(r'(\d+)$', last_invoice_number)

        if match:
            # Нашли число в конце
            number_part = match.group(1)
            # Префикс - это все, что было до числа
            prefix = last_invoice_number[:-len(number_part)]
            # Увеличиваем число и соединяем с префиксом
            next_number = int(number_part) + 1
            return f"{prefix}{next_number}"
        else:
            # Числа в конце нет, возможно, номер - это просто число
            try:
                next_number = int(last_invoice_number) + 1
                return str(next_number)
            except (ValueError, TypeError):
                # Не удалось преобразовать в число, возвращаем как есть с суффиксом
                return f"{last_invoice_number}-1"

    def get_form_kwargs(self):
        """
        Передает начальные данные в форму, включая номер счета и данные из GET-запроса.
        """
        kwargs = super().get_form_kwargs()

        # Готовим словарь для начальных данных
        initial_data = {}

        # Если это GET-запрос, добавляем сгенерированный номер счета
        if self.request.method == 'GET':
            initial_data['invoice_number'] = self.get_next_invoice_number()

        # Добавляем все данные из GET-параметров, если они есть
        # self.request.GET - это QueryDict, который ведет как словарь
        for field in self.form_class.base_fields:
            if field in self.request.GET:
                initial_data[field] = self.request.GET.get(field)

        # Обновляем kwargs с начальными данными
        kwargs['initial'] = initial_data

        return kwargs


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "frontend/order_list.html"
    context_object_name = "orders"
    paginate_by = 20
    ordering = "-id"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("driver", "actual_vehicle")
        )


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "frontend/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("driver", "actual_vehicle")
        )


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = "frontend/order_form.html"
    form_class = OrderForm

    def get_success_url(self):
        return reverse("frontend:order_detail", kwargs={"pk": self.object.pk})


class RouteListView(LoginRequiredMixin, ListView):
    model = Route
    template_name = "frontend/route_list.html"
    context_object_name = "routes"
    paginate_by = 20
    ordering = "-date_start"


class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = "frontend/route_detail.html"
    context_object_name = "route"

    def get_queryset(self):
        return super().get_queryset().select_related('vehicle', 'driver')


class RouteUpdateView(LoginRequiredMixin, RouteContextMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = "frontend/route_form.html"

    def get_success_url(self):
        return reverse("frontend:route_detail", kwargs={"pk": self.object.pk})

class OrderCopyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        source_order = get_object_or_404(Order, pk=self.kwargs['pk'])

        data_to_copy = {
            'description': source_order.description,
            'customer': source_order.customer,
            'route_from': source_order.route_from,
            'route_to': source_order.route_to,
            'places': source_order.places,
            'weight_kg': source_order.weight_kg,
            'volume_m3': source_order.volume_m3,
            'rate': source_order.rate,
            'vat_status': source_order.vat_status,
            'notes': f"Скопировано из заявки {source_order.code}",
            'document_driver': source_order.document_driver,
            'document_vehicle': source_order.document_vehicle,
        }

        all_codes = Order.objects.filter(
            code__regex=r'^\d+[cс]$'
        ).values_list('code', flat=True)

        max_num = 0
        for code_str in all_codes:
            try:
                num = int(code_str[:-1])
                if num > max_num:
                    max_num = num
            except (ValueError, IndexError):
                continue

        new_code = f"{max_num + 1}c"

        data_to_copy['code'] = new_code

        base_url = reverse('frontend:add_order')
        cleaned_data = {k: v for k, v in data_to_copy.items() if v is not None and v != ''}
        query_string = urlencode(cleaned_data)
        redirect_url = f'{base_url}?{query_string}'

        return HttpResponseRedirect(redirect_url)

        return HttpResponseRedirect(redirect_url)