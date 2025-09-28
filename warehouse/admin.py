from django.contrib import admin
from .models import Cargo

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "vat_status", "is_return_trip")
    list_filter = ("vat_status", "is_return_trip")
    search_fields = ("code", "description")