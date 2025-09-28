from django.urls import path
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("orders/new/", views.RouteCreateView.as_view(), name="route_create"),
    path("drivers/new/", views.DriverCreateView.as_view(), name="driver_create"),
]