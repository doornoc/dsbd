from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager, Group, GroupManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class CustomGroup(Group):
    class Meta:
        verbose_name = 'group'
        verbose_name_plural = "groups"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    date_joined = models.DateTimeField("date joined", default=timezone.now)
    username = models.CharField("username", max_length=150, validators=[username_validator], unique=True)
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    email = models.EmailField("email", unique=True)
    is_staff = models.BooleanField("管理者ステータス", default=False)
    is_member = models.BooleanField("会員ステータス", default=False)
    is_active = models.BooleanField("アカウントステータス", default=True)
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
        verbose_name = "user"
        verbose_name_plural = "users"

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
