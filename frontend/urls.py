from django.urls import path
from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("orders/", views.OrderListView.as_view(), name="orders_list"),
    path("orders/new/", views.OrderCreateView.as_view(), name="add_order"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/edit/", views.OrderUpdateView.as_view(), name="order_edit"),
    path("routes/new/", views.RouteCreateView.as_view(), name="add_route"),
    path("drivers/new/", views.DriverCreateView.as_view(), name="add_driver"),
]