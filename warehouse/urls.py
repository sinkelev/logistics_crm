from django.urls import path
from .views import (
    PostalRecordListView, PostalRecordCreateView,
    PostalRecordUpdateView, PostalRecordDetailView,
)

app_name = "warehouse"

urlpatterns = [
    path("postals/", PostalRecordListView.as_view(), name="postal_list"),
    path("postals/new/", PostalRecordCreateView.as_view(), name="postal_create"),
    path("postals/<int:pk>/", PostalRecordDetailView.as_view(), name="postal_detail"),
    path("postals/<int:pk>/edit/", PostalRecordUpdateView.as_view(), name="postal_edit"),
]