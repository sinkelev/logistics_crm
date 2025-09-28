from django.conf import settings
from rest_framework import serializers
from .models import Expense
from accounts.models import User
from logistics.models import Route
from vehicles.models import Vehicle


class ExpenseSerializer(serializers.ModelSerializer):
    route_number = serializers.CharField(
        source="route.route_number",
        read_only=True,
    )
    vehicle_label = serializers.CharField(
        source="vehicle.__str__",
        read_only=True,
    )
    employee_name = serializers.CharField(
        source="employee.get_full_name",
        read_only=True,
    )
    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True,
    )

    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(),
        allow_null=True,
        required=False,
    )
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        allow_null=True,
        required=False,
    )
    employee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Expense
        fields = [
            "id",
            "route",
            "route_number",
            "vehicle",
            "vehicle_label",
            "employee",
            "employee_name",
            "category",
            "category_display",
            "amount",
            "incurred_at",
            "description",
            "document",
            "created_at",
        ]
        read_only_fields = ["created_at"]