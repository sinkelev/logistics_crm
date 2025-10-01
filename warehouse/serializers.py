from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    vat_status_display = serializers.CharField(
        source="get_vat_status_display",
        read_only=True,
    )
    driver_name = serializers.CharField(
        source="driver.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "code",
            "order_number",
            "description",
            "places",
            "weight_kg",
            "volume_m3",
            "rate",
            "customer",
            "vat_status",
            "vat_status_display",
            "is_return_trip",
            "invoice_number",
            "act_number",
            "invoice_act_number",
            "driver",
            "driver_name",
            "document_driver",
            "route_from",
            "route_to",
        ]