# logistics/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from logistics.models import Route, RouteCargo
from warehouse.models import Order


@receiver(post_save, sender=RouteCargo)
def assign_driver_on_routecargo_save(sender, instance, **kwargs):
    """
    При привязке заявки к маршруту синхронизируем водителя.
    """
    cargo = instance.cargo
    new_driver = instance.route.driver

    if cargo.driver != new_driver:
        cargo.driver = new_driver
        cargo.save(update_fields=['driver'])


@receiver(post_delete, sender=RouteCargo)
def clear_driver_on_routecargo_delete(sender, instance, **kwargs):
    """
    Если заявку отвязали от маршрута, у которого был водитель, и она больше ни к одному маршруту не привязана — очищаем поле.
    """
    if not RouteCargo.objects.filter(cargo_id=instance.cargo_id).exists():
        Order.objects.filter(pk=instance.cargo_id).update(driver_id=None)


@receiver(post_save, sender=Route)
def assign_driver_on_route_save(sender, instance, **kwargs):
    """
    При сохранении маршрута (создание/изменение) синхронизируем водителя со всеми его заявками.
    """
    Order.objects.filter(routecargo__route=instance).update(driver_id=instance.driver_id)

@receiver(post_save, sender=Route)
def update_driver_on_route_save(sender, instance, **kwargs):
    """Обновляет водителя во всех заявках маршрута"""
    if instance.driver:
        Order.objects.filter(routecargo__route=instance).update(driver=instance.driver)