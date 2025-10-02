import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
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


class RouteCreateView(LoginRequiredMixin, CreateView):
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
        """Передаем начальное значение для номера счета в форму."""
        kwargs = super().get_form_kwargs()
        # Этот метод вызывается только для GET-запросов (не при отправке формы)
        if self.request.method == 'GET':
            kwargs['initial_invoice_number'] = self.get_next_invoice_number()
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


class RouteUpdateView(LoginRequiredMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = "frontend/route_form.html"

    def get_success_url(self):
        return reverse("frontend:route_detail", kwargs={"pk": self.object.pk})