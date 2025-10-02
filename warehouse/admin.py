from django.contrib import admin
from .models import Order, WarehouseEntry

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'order_number', 'customer', 'weight_kg', 'places', 'rate',
        'vat_status', 'is_return_trip', 'driver', 'document_driver',
        'actual_vehicle', 'document_vehicle', 'route_from', 'route_to'
    )
    list_filter = ('vat_status', 'is_return_trip', 'driver', 'actual_vehicle')
    search_fields = ('code', 'customer', 'description',
                     'document_driver__username','document_driver', 'document_vehicle')
    raw_id_fields = ('driver', 'actual_vehicle',)

@admin.register(WarehouseEntry)
class WarehouseEntryAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'arrived_at', 'released_at', 'location', 'storage_time_hours')
    list_filter = ('arrived_at', 'released_at', 'location')
    search_fields = ('cargo__code', 'location', 'notes')
    date_hierarchy = 'arrived_at'