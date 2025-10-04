from django.urls import path, include
from . import views


app_name = "frontend"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("orders/", views.OrderListView.as_view(), name="orders_list"),
    path("orders/new/", views.OrderCreateView.as_view(), name="add_order"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/edit/", views.OrderUpdateView.as_view(), name="order_edit"),
    path("orders/<int:pk>/copy/", views.OrderCopyView.as_view(), name="order_copy"),
    path("routes/new/", views.RouteCreateView.as_view(), name="add_route"),
    path("routes/", views.RouteListView.as_view(), name="routes_list"),
    path("routes/<int:pk>/", views.RouteDetailView.as_view(), name="route_detail"),
    path("routes/<int:pk>/edit/", views.RouteUpdateView.as_view(), name="route_edit"),
    path("vehicles/cars/", views.VehicleListView.as_view(vehicle_type='cars'), name="vehicle_car_list"),
    path("vehicles/trailers/", views.VehicleListView.as_view(vehicle_type='trailers'), name="vehicle_trailer_list"),
    path("vehicles/new/", views.VehicleCreateView.as_view(), name="vehicle_create"),
    path("vehicles/<int:pk>/", views.VehicleDetailView.as_view(), name="vehicle_detail"),
    path("vehicles/<int:pk>/edit/", views.VehicleUpdateView.as_view(), name="vehicle_edit"),
    path("accounts/", include("accounts.urls")),
]