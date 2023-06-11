from django.db import models
from django.db.models import Q
from django.utils import timezone

from custom_auth.models import CustomGroup
from dsbd.models import MediumTextField


class ServiceManager(models.Manager):
    def get_service(self, groups):
        q = Q()
        q &= Q(is_active=True)

        for group in groups:
            q.add(Q(group=group), Q.OR)
        return self.filter(q)


class Service(models.Model):
    OneIPByWireguard = "Wireguardによる接続"
    ETC = "その他"

    TYPE1_CHOICES = (
        (OneIPByWireguard, OneIPByWireguard),
        (ETC, ETC),
    )

    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日", default=timezone.now, db_index=True)
    start_at = models.DateTimeField("サービス開始日", blank=True, null=True)
    end_at = models.DateTimeField("サービス終了日", blank=True, null=True)
    is_active = models.BooleanField("有効", default=True)
    type1 = models.CharField("type1", max_length=200, choices=TYPE1_CHOICES)
    content = MediumTextField(verbose_name="内容", default="", blank=True)

    objects = ServiceManager()
