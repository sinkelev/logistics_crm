from django.contrib import admin
from .models import Order, WarehouseEntry

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'customer', 'consignee', 'weight_kg', 'volume_m3',
        'vat_status', 'is_return_trip', 'driver', 'document_driver', 'route_from', 'route_to'
    )
    list_filter = ('vat_status', 'is_return_trip', 'driver')
    search_fields = ('code', 'customer', 'consignee', 'description', 'document_driver')
    # Добавлено 'driver' в raw_id_fields, чтобы упростить выбор водителя из большого списка
    raw_id_fields = ('driver',)

@admin.register(WarehouseEntry)
class WarehouseEntryAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'arrived_at', 'released_at', 'location', 'storage_time_hours')
    list_filter = ('arrived_at', 'released_at', 'location')
    search_fields = ('cargo__code', 'location', 'notes')
    date_hierarchy = 'arrived_at'