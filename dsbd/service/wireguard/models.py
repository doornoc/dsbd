from django.core import validators
from django.db import models
from django.utils import timezone

from custom_auth.models import Group
from dsbd.service.models import Service as main_service


class ServiceManager(models.Manager):
    print("")


class Server(models.Model):
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    is_active = models.BooleanField("有効", default=True)
    start_ip = models.GenericIPAddressField("Start IP", )
    size = models.IntegerField("Size", validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(32)
    ])
    gateway_ip = models.GenericIPAddressField("Gateway IP(Local)", )
    global_ip = models.GenericIPAddressField("Global IP", )
    global_port = models.IntegerField("Global Port", default=51820)
    mgmt_ip = models.GenericIPAddressField("Management IP", )
    mgmt_port = models.IntegerField("Management Port", default=8080)
    private_key = models.CharField("秘密鍵", max_length=250)
    public_key = models.CharField("公開鍵", max_length=250)

    class Meta:
        verbose_name = 'Wireguardサーバ'
        verbose_name_plural = "Wireguardサーバ"

    def __str__(self):
        return "%d: (GIP: %s) (MIP:%s)" % (self.id, self.global_ip, self.mgmt_ip)


class Service(models.Model):
    service = models.OneToOneField(main_service, on_delete=models.CASCADE, related_name="wireguard_service")
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    is_active = models.BooleanField("有効", default=True)
    ipv4 = models.GenericIPAddressField("IPv4", blank=True, null=True)
    ipv6 = models.GenericIPAddressField("IPv6", blank=True, null=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    public_key = models.CharField("公開鍵", max_length=250)

    objects = ServiceManager()

    class Meta:
        verbose_name = 'Wireguardサービス'
        verbose_name_plural = "Wireguardサービス"

    def __str__(self):
        return "%d: %s,%s" % (self.id, self.ipv4, self.ipv6)
