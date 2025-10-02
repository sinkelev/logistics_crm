from django.contrib import admin
from .models import Route, RouteCargo

class RouteCargoInline(admin.TabularInline):
    model = RouteCargo
    extra = 1

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("route_number", "vehicle", "driver", "date_start", "legal_entity")
    list_filter = ("legal_entity", "vehicle__is_collector")
    search_fields = ("route_number", "vehicle__plate_number", "driver__username")
    inlines = [RouteCargoInline]