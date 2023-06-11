import uuid

from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, AbstractUser, Group, GroupManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, key, username, email, password, **extra_fields):
        if not SignUpKey.objects.check_key(key):
            raise ValueError("認証キーが一致しません")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        user = self._create_user(username, email, password, **extra_fields)
        user_activate_token = UserActivateToken.objects.create(
            user=user
        )
        subject = 'Please Activate Your Account'
        message = f'URLにアクセスしてアカウントを有効化してください。\n {settings.DOMAIN_URL}/activate/{user_activate_token.token}/'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email, ]
        send_mail(subject, message, from_email, recipient_list)
        SignUpKey.objects.used_key(key)

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    created_at = models.DateTimeField("date joined", default=timezone.now)
    username = models.CharField("username", max_length=150, validators=[username_validator], unique=True)
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    email = models.EmailField("email", unique=True)
    is_staff = models.BooleanField("管理者ステータス", default=False)
    is_member = models.BooleanField("会員ステータス", default=False)
    is_active = models.BooleanField("アカウントステータス", default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name='Group',
        blank=True,
        help_text='Specific Groups for this user.',
        related_name="user_set",
        related_query_name="user",
    )
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "ユーザ"
        verbose_name_plural = "ユーザ"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.username


def user_activate_expire_date():
    return timezone.now() + timezone.timedelta(days=settings.USER_ACTIVATE_EXPIRED_DAYS)


class UserActivateTokensManager(models.Manager):
    def activate_user_by_token(self, activate_token):
        user_activate_token = self.filter(token=activate_token, expired_at__gt=timezone.now()).first()
        if user_activate_token.is_used:
            return {"error": "this token was used..."}
        if hasattr(user_activate_token, 'user'):
            user = user_activate_token.user
            user.is_active = True
            user.save()
            user_activate_token.is_used = True
            user_activate_token.save()
            return {"user": user, "error": ""}


class UserActivateToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField("Active token", default=uuid.uuid4)
    expired_at = models.DateTimeField("有効期限", default=user_activate_expire_date)
    is_used = models.BooleanField("使用済み", default=False)

    objects = UserActivateTokensManager()

    class Meta:
        verbose_name = 'Activate用のToken'
        verbose_name_plural = "Activate用のToken"


def sign_up_key_expire_date():
    return timezone.now() + timezone.timedelta(days=settings.SIGN_UP_EXPIRED_DAYS)


class SignUpKeyManager(models.Manager):
    def check_key(self, key):
        try:
            sign_up_key = self.filter(key=key, expired_at__gt=timezone.now(), is_used=False).first()
        except:
            return False
        # keyがない時
        if not sign_up_key:
            return False
        return True

    def used_key(self, key):
        sign_up_key = self.filter(key=key, is_used=False).first()
        # keyがない時
        if not sign_up_key:
            return False
        sign_up_key.is_used = True
        sign_up_key.save()
        return True


class SignUpKey(models.Model):
    key = models.UUIDField("認証キー", default=uuid.uuid4, editable=True)
    comment = models.CharField("コメント", max_length=200, default="", blank=True)
    expired_at = models.DateTimeField("有効期限", default=sign_up_key_expire_date)
    is_used = models.BooleanField("使用済み", default=False)

    objects = SignUpKeyManager()

    class Meta:
        verbose_name = 'サインアップ用のKey'
        verbose_name_plural = "サインアップ用のKey"


class CustomGroupManager(models.Manager):
    def active_filter(self):
        return self.filter(is_active=True)


class CustomGroup(Group):
    is_active = models.BooleanField("アカウントステータス", default=False)
    admin_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField("comment", max_length=250, default="", blank=True)

    objects = CustomGroupManager()

    class Meta:
        verbose_name = 'グループ'
        verbose_name_plural = "グループ"

    def __str__(self):
        return self.name
