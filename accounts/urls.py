from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("drivers/", views.DriverListView.as_view(), name="driver_list"),
    path("drivers/new/", views.DriverCreateView.as_view(), name="driver_create"),
    path("drivers/<int:pk>/", views.DriverDetailView.as_view(), name="driver_detail"),
    path("drivers/<int:pk>/edit/", views.DriverUpdateView.as_view(), name="driver_edit"),
]