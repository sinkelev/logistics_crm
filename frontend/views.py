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


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order # Указываем модель, для которой создаем объект
    template_name = "frontend/order_form.html"
    form_class = OrderForm # Используем нашу OrderForm
    success_url = reverse_lazy("frontend:dashboard") # Перенаправляем на дашборд после сохранения


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
            .select_related("driver", "document_driver")
        )


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "frontend/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("driver", "document_driver")
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
    ordering = "-planned_start"


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