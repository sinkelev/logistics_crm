from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "incurred_at", "route", "vehicle", "employee")
    list_filter = ("category", "incurred_at")
    search_fields = ("description", "route__route_number", "vehicle__plate_number")