from django.urls import path
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("orders/new/", views.OrderCreateView.as_view(), name="add_order"),
    path("routes/new/", views.RouteCreateView.as_view(), name="add_route"),
    path("drivers/new/", views.DriverCreateView.as_view(), name="add_driver"), ]