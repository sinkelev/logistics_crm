from django.contrib import admin
from .models import Order, WarehouseEntry

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'order_number', 'customer', 'weight_kg', 'places', 'rate', # Добавлены places и rate
        'vat_status', 'is_return_trip', 'driver', 'document_driver', 'route_from', 'route_to'
    )
    list_filter = ('vat_status', 'is_return_trip', 'driver', 'document_driver')
    search_fields = ('code', 'customer', 'description', 'document_driver__username')
    raw_id_fields = ('driver', 'document_driver',)

@admin.register(WarehouseEntry)
class WarehouseEntryAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'arrived_at', 'released_at', 'location', 'storage_time_hours')
    list_filter = ('arrived_at', 'released_at', 'location')
    search_fields = ('cargo__code', 'location', 'notes')
    date_hierarchy = 'arrived_at'