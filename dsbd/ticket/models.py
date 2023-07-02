from django.db import models
from django.db.models import Q

from custom_auth.models import User, Group
from dsbd.models import MediumTextField


class TemplateManager(models.Manager):
    def get_template(self):
        return self.filter(is_active=True).order_by('type1', 'type2')


class Template(models.Model):
    id = models.IntegerField("ID", auto_created=True, primary_key=True, editable=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True, db_index=True)
    is_active = models.BooleanField("有効", default=True)
    type1 = models.CharField("type1", max_length=200)
    type2 = models.CharField("type2", max_length=200, default='', blank=True)
    title = models.CharField("title", max_length=250)
    body = MediumTextField(verbose_name="内容", default="", blank=True)
    comment = models.CharField("comment", max_length=250, default='')

    objects = TemplateManager()

    class Meta:
        verbose_name = 'チケットテンプレート'
        verbose_name_plural = "チケットテンプレート"

    def __str__(self):
        return "%d: (%s:%s)%s" % (self.id, self.type1, self.type2, self.title)


class TicketManager(models.Manager):
    def get_ticket(self, user):
        q = Q()
        q.add(Q(user=user), Q.OR)
        group_filter = user.groups.filter(is_active=True)
        if group_filter.exists():
            for group in user.groups.filter(is_active=True).all():
                q.add(Q(group=group), Q.OR)
        tickets = self.filter(q).order_by('is_solved', 'id')
        return tickets

    def get_one_ticket(self, ticket_id, user):
        q = Q()
        q.add(Q(user=user), Q.OR)
        group_filter = user.groups.filter(is_active=True)
        if group_filter.exists():
            for group in user.groups.filter(is_active=True).all():
                q.add(Q(group=group), Q.OR)
        return self.filter(id=ticket_id).filter(q).first()

    def get_chat(self, ticket_id):
        return self.get(id=ticket_id).chat_set.all()


class Ticket(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    title = models.CharField("title", max_length=250)
    body = MediumTextField(verbose_name="内容", default="", blank=True)
    is_solved = models.BooleanField("解決済み", default=False)
    is_approve = models.BooleanField("承認済み", default=False)
    is_reject = models.BooleanField("拒否済み", default=False)
    from_admin = models.BooleanField("運営委員から起票", default=False)

    objects = TicketManager()

    class Meta:
        verbose_name = 'チケット'
        verbose_name_plural = "チケット"

    def __str__(self):
        group_name = "none"
        if self.group:
            group_name = self.group.name
        return "%d[%s:%s]: %s" % (
            self.id,
            self.user.username,
            group_name,
            self.title
        )


class Chat(models.Model):
    created_at = models.DateTimeField("作成日", auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    body = MediumTextField(verbose_name="内容", default="", blank=True)
    is_admin = models.BooleanField("運営委員がコメント", default=False)

    class Meta:
        verbose_name = 'チャット'
        verbose_name_plural = "チャット"

    def __str__(self):
        return "%d[%d]" % (self.id, self.ticket.id)
