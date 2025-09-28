from rest_framework import serializers
from .models import Cargo


class CargoSerializer(serializers.ModelSerializer):
    vat_status_display = serializers.CharField(
        source="get_vat_status_display",
        read_only=True,
    )

    class Meta:
        model = Cargo
        fields = [
            "id",
            "code",
            "description",
            "weight_kg",
            "volume_m3",
            "shipper",
            "consignee",
            "vat_status",
            "vat_status_display",
            "is_return_trip",
        ]