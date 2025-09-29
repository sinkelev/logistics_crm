from django.core.management.base import BaseCommand
from django.utils import timezone
from vehicles.models import Vehicle
from accounts.models import User
from logistics.models import Route
from warehouse.models import Order

class Command(BaseCommand):
    def handle(self, *args, **options):
        Vehicle.objects.get_or_create(plate_number="A123BC", brand="Volvo", model="FH", payload_capacity_kg=20000)
        User.objects.get_or_create(username="driver1", defaults={"role": "driver"})
        Order.objects.get_or_create(
            code="ORDER-001",
            defaults={
                "description": "Швеллеры 5т",
                "weight_kg": 5000,
                "customer": "Заказчик Пример",
                "consignee": "Получатель Пример",
                "route_from": "Москва",
                "route_to": "Санкт-Петербург"
            }
        )
        Route.objects.get_or_create(route_number="R-2024-0001", planned_start=timezone.now())
        self.stdout.write(self.style.SUCCESS("Demo data installed"))