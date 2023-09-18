from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from custom_auth.models import Group, User, SignUpKey
from dsbd.notify import notify_db_save


@receiver(pre_save, sender=Group)
def group_model_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = Group.objects.get(pk=instance.pk)
    except Group.DoesNotExist:
        instance._pre_save_instance = instance


@receiver(post_save, sender=Group)
def post_group(sender, instance, created, **kwargs):
    if created:
        text = get_create_group(True, instance)
        notify_db_save(table_name="Group", type=0, data=text)
    else:
        text = get_update_group(instance._pre_save_instance, instance)
        notify_db_save(table_name="Group", type=1, data=text)


@receiver(pre_delete, sender=Group)
def delete_group(sender, instance, **kwargs):
    text = get_create_group(False, instance)
    notify_db_save(table_name="Group", type=2, data=text)


def get_create_group(short, instance):
    text = '--%d[%s]--\n' % (instance.id, instance.name,)
    return text if not short else text + '有効: %r\n課金: %r\n有効期限: %s\n郵便番号: %s\nE-Mail: %s\n' % (
        instance.is_active, instance.is_charge, instance.expired_at, instance.zipcode, instance.email)


def get_update_group(before, after):
    text = '%s----更新状況----\n' % (get_create_group(True, before),)
    if before.name != after.name:
        text += 'name: %s => %s\n' % (before.name, after.name)
    if before.is_active != after.is_active:
        text += '有効: %r => %r\n' % (before.is_active, after.is_active)
    if before.is_charge != after.is_charge:
        text += '課金: %r => %r\n' % (before.is_charge, after.is_charge)
    if before.expired_at != after.expired_at:
        text += '有効期限: %s => %s\n' % (before.expired_at, after.expired_at)
    if before.stripe_customer_id != after.stripe_customer_id:
        text += 'Stripe(Customer): %s => %s\n' % (before.stripe_customer_id, after.stripe_customer_id)
    if before.stripe_subscription_id != after.stripe_subscription_id:
        text += 'Stripe(Subscribe): %s => %s\n' % (before.stripe_subscription_id, after.stripe_subscription_id)
    if before.zipcode != after.zipcode:
        text += '郵便番号: %s => %s\n' % (before.zipcode, after.zipcode)
    if before.address != after.address:
        text += '住所: %s => %s\n' % (before.address, after.address)
    if before.address_en != after.address_en:
        text += '住所(En): %s => %s\n' % (before.address_en, after.address_en)
    if before.email != after.email:
        text += 'E-Mail: %s => %s\n' % (before.email, after.email)
    if before.phone != after.phone:
        text += '電話番号: %s => %s\n' % (before.phone, after.phone)
    if before.country != after.country:
        text += '国籍: %s => %s\n' % (before.country, after.country)
    text += '------------\n'
    return text


@receiver(pre_save, sender=User)
def user_model_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        instance._pre_save_instance = instance


@receiver(post_save, sender=User)
def post_user(sender, instance, created, **kwargs):
    if created:
        text = get_create_user(True, instance)
        notify_db_save(table_name="User", type=0, data=text)
    else:
        text = get_update_user(instance._pre_save_instance, instance)
        notify_db_save(table_name="User", type=1, data=text)


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    text = get_create_user(False, instance)
    notify_db_save(table_name="User", type=2, data=text)


def get_create_user(short, instance):
    text = '--%d[%s]--\n' % (instance.id, instance.username,)
    return text if not short else text + '有効: %r\n課金: %r\n有効期限: %s\nE-Mail: %s\n' % (
        instance.is_active, instance.is_charge, instance.expired_at, instance.email)


def get_update_user(before, after):
    text = '%s----更新状況----\n' % (get_create_user(True, before),)
    if before.username != after.username:
        text += 'username: %s => %s\n' % (before.username, after.username)
    if before.first_name != after.first_name:
        text += '住所: %s => %s\n' % (before.first_name, after.first_name)
    if before.last_name != after.last_name:
        text += '住所(En): %s => %s\n' % (before.last_name, after.last_name)
    if before.email != after.email:
        text += 'E-Mail: %s => %s\n' % (before.email, after.email)
    if before.is_active != after.is_active:
        text += '有効: %r => %r\n' % (before.is_active, after.is_active)
    if before.is_charge != after.is_charge:
        text += '課金: %r => %r\n' % (before.is_charge, after.is_charge)
    if before.expired_at != after.expired_at:
        text += '有効期限: %s => %s\n' % (before.expired_at, after.expired_at)
    if before.stripe_customer_id != after.stripe_customer_id:
        text += 'Stripe(Customer): %s => %s\n' % (before.stripe_customer_id, after.stripe_customer_id)
    if before.stripe_subscription_id != after.stripe_subscription_id:
        text += 'Stripe(Subscribe): %s => %s\n' % (before.stripe_subscription_id, after.stripe_subscription_id)
    if before.add_group != after.add_group:
        text += 'グループ追加: %r => %r\n' % (before.add_group, after.add_group)
    text += '------------\n'
    return text


@receiver(pre_save, sender=SignUpKey)
def signup_key_model_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = SignUpKey.objects.get(pk=instance.pk)
    except SignUpKey.DoesNotExist:
        instance._pre_save_instance = instance


@receiver(post_save, sender=SignUpKey)
def post_signup_key(sender, instance, created, **kwargs):
    if created:
        text = get_create_signup_key(True, instance)
        notify_db_save(table_name="SignUpKey", type=0, data=text)
    else:
        text = get_update_signup_key(instance._pre_save_instance, instance)
        notify_db_save(table_name="SignUpKey", type=1, data=text)


@receiver(pre_delete, sender=SignUpKey)
def delete_signup_key(sender, instance, **kwargs):
    text = get_create_signup_key(False, instance)
    notify_db_save(table_name="SignUpKey", type=2, data=text)


def get_create_signup_key(short, instance):
    text = '--%d[%s]--\n' % (instance.id, instance.key,)
    return text if not short else text + '利用済み: %r\n有効期限: %s\n' % (instance.is_used, instance.expired_at)


def get_update_signup_key(before, after):
    text = '%s----更新状況----\n' % (get_create_signup_key(True, before),)
    if before.key != after.key:
        text += 'key: %s => %s\n' % (before.key, after.key)
    if before.is_used != after.is_used:
        text += '使用済み: %r => %r\n' % (before.is_used, after.is_used)
    if before.expired_at != after.expired_at:
        text += '有効期限: %s => %s\n' % (before.expired_at, after.expired_at)
    if before.comment != after.comment:
        text += 'comment: %r => %r\n' % (before.comment, after.comment)
    text += '------------\n'
    return text
