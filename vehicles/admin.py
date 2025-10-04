from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "brand", "model", "status", "is_collector")
    list_filter = ("status", "is_collector")
    search_fields = ("plate_number", "vin", "brand", "model")