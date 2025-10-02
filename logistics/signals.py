from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Route, RouteCargo
from warehouse.models import Order


@receiver(post_save, sender=RouteCargo)
def sync_order_from_routecargo(sender, instance, **kwargs):
    """
    При привязке заявки к маршруту (через RouteCargo)
    синхронизируем водителя и машину по факту.
    """
    cargo = instance.cargo
    route = instance.route

    update_data = {}

    if cargo.driver != route.driver:
        update_data['driver'] = route.driver

    if cargo.actual_vehicle != route.vehicle:
        update_data['actual_vehicle'] = route.vehicle

    if update_data:
        # Используем .update() чтобы не вызывать .save() на заявке и избежать рекурсии
        Order.objects.filter(pk=cargo.pk).update(**update_data)


@receiver(post_delete, sender=RouteCargo)
def clear_order_details_on_routecargo_delete(sender, instance, **kwargs):
    """
    Если заявку отвязали от маршрута и она больше ни к одному маршруту не привязана —
    очищаем поля водителя и машины по факту.
    """
    if not RouteCargo.objects.filter(cargo_id=instance.cargo_id).exists():
        Order.objects.filter(pk=instance.cargo_id).update(driver_id=None, actual_vehicle_id=None)


@receiver(post_save, sender=Route)
def sync_orders_on_route_save(sender, instance, **kwargs):
    """
    При изменении маршрута (например, смена водителя или ТС)
    синхронизируем водителя и машину во всех привязанных заявках.
    """
    orders_on_route = Order.objects.filter(routecargo__route=instance)

    # Обновляем водителя, где он отличается
    orders_on_route.exclude(driver=instance.driver).update(driver=instance.driver)

    # Обновляем машину, где она отличается
    orders_on_route.exclude(actual_vehicle=instance.vehicle).update(actual_vehicle=instance.vehicle)