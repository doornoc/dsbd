from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from dsbd.service.wireguard.api import wg_all_delete, wg_delete, wg_overwrite, wg_create, wg_update
from dsbd.service.wireguard.models import Service, Server


@receiver(pre_save, sender=Server)
def update_server(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        prev = Server.objects.get(id=instance.id)
        if prev.is_active != instance.is_active:
            if instance.is_active:
                wg_overwrite(instance)
            else:
                wg_all_delete(instance)


@receiver(pre_delete, sender=Service)
def delete_server(sender, instance, **kwargs):
    wg_all_delete(instance)


@receiver(pre_save, sender=Service)
def update_service(sender, instance, **kwargs):
    try:
        if instance.id is None:
            wg_create(instance.server, instance)
            pass
        else:
            prev = Server.objects.get(id=instance.id)
            if prev.is_active != instance.is_active:
                if instance.is_active:
                    wg_create(instance.server, instance)
                else:
                    wg_delete(instance.server, instance.public_key)
            elif prev.public_key != instance.public_key:
                wg_update(instance.server, prev.public_key, instance)
    except:
        print("ERROR")


@receiver(pre_delete, sender=Service)
def delete_service(sender, instance, created, **kwargs):
    wg_delete(instance.server, instance.public_key)
