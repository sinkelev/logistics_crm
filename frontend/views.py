from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from logistics.models import Route
from logistics.forms import RouteForm
from accounts.models import User
from accounts.forms import DriverForm
from warehouse.models import Order # <-- Добавлено
from warehouse.forms import OrderForm # <-- Добавлено

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_routes"] = Route.objects.select_related("vehicle", "driver").order_by("-planned_start")[:5]
        context["drivers_count"] = User.objects.filter(role="driver").count()
        # Можно добавить статистику по заявкам, если нужно
        # context["orders_count"] = Order.objects.count()
        return context


class RouteCreateView(LoginRequiredMixin, CreateView):
    template_name = "frontend/route_form.html"
    form_class = RouteForm
    success_url = reverse_lazy("frontend:dashboard")


class DriverCreateView(LoginRequiredMixin, CreateView):
    template_name = "frontend/driver_form.html"
    form_class = DriverForm
    success_url = reverse_lazy("frontend:dashboard")


# НОВОЕ ПРЕДСТАВЛЕНИЕ ДЛЯ ЗАЯВКИ
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order # Указываем модель, для которой создаем объект
    template_name = "frontend/order_form.html"
    form_class = OrderForm # Используем нашу OrderForm
    success_url = reverse_lazy("frontend:dashboard") # Перенаправляем на дашборд после сохранения
