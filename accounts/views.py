from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .forms import DriverForm


class DriverListView(LoginRequiredMixin, ListView):
    model = User
    queryset = User.objects.filter(role="driver")
    template_name = "frontend/driver_list.html"
    context_object_name = "drivers"


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = User
    queryset = User.objects.filter(role="driver")
    template_name = "frontend/driver_detail.html"
    context_object_name = "driver"


class DriverUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = DriverForm
    template_name = "frontend/driver_form.html"

    def get_success_url(self):
        return reverse_lazy("accounts:driver_detail", kwargs={"pk": self.object.pk})


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = DriverForm
    template_name = "frontend/driver_form.html"
    success_url = reverse_lazy("accounts:driver_list")

    def form_valid(self, form):
        form.instance.role = "driver"
        return super().form_valid(form)