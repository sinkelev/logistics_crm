from rest_framework import serializers
from .models import Route, RouteCargo
from warehouse.models import Cargo
from warehouse.serializers import CargoSerializer


class RouteCargoSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer(read_only=True)

    class Meta:
        model = RouteCargo
        fields = [
            "id",
            "cargo",
            "position",
            "is_collected_by_collector",
        ]


class RouteSerializer(serializers.ModelSerializer):
    cargo_items = RouteCargoSerializer(
        source="routecargo_set",
        many=True,
        read_only=True,
    )
    cargoes = serializers.PrimaryKeyRelatedField(
        queryset=Cargo.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    vehicle_label = serializers.CharField(
        source="vehicle.__str__",
        read_only=True,
    )
    driver_label = serializers.CharField(
        source="driver.__str__",
        read_only=True,
    )
    legal_entity_display = serializers.CharField(
        source="get_legal_entity_display",
        read_only=True,
    )

    class Meta:
        model = Route
        fields = [
            "id",
            "route_number",
            "vehicle",
            "vehicle_label",
            "driver",
            "driver_label",
            "planned_start",
            "planned_end",
            "actual_start",
            "actual_end",
            "legal_entity",
            "legal_entity_display",
            "distance_km",
            "notes",
            "cargoes",       # для записи (список id грузов)
            "cargo_items",   # для чтения (с деталями и позициями)
        ]

    def create(self, validated_data):
        cargoes = validated_data.pop("cargoes", [])
        route = super().create(validated_data)
        self._replace_cargo_links(route, cargoes)
        return route

    def update(self, instance, validated_data):
        cargoes = validated_data.pop("cargoes", None)
        route = super().update(instance, validated_data)
        if cargoes is not None:
            self._replace_cargo_links(route, cargoes)
        return route

    def _replace_cargo_links(self, route, cargoes):
        RouteCargo.objects.filter(route=route).delete()
        for index, cargo in enumerate(cargoes, start=1):
            RouteCargo.objects.create(
                route=route,
                cargo=cargo,
                position=index,
            )