"""
Django settings for dsbd project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from importlib import import_module
from pathlib import Path
import os

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from dsbd.templatetags import extra


def _import_ldap_group_type(group_type_name):
    mod = import_module('django_auth_ldap.config')
    try:
        return getattr(mod, group_type_name)()
    except:
        return None


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4$6)p#4&_5j$15ip+0-mq+ji@wy%s2i^y)6*pa#tw4k3o8iho7')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(' ')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000').split(' ')

SITE_TITLE = os.environ.get('SITE_TITLE', 'doornoc Dashboard')
SITE_HEADER = os.environ.get('SITE_HEADER', 'doornoc Dashboard')

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'custom_auth',
    'widget_tweaks',
    'dsbd.notice',
    'dsbd.service',
    'dsbd.service.wireguard',
    'dsbd.ticket',
    'dsbd.custom_admin'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
]

ROOT_URLCONF = 'dsbd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'dsbd/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['dsbd.templatetags.extra'],
        },
    },
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'dsbd/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

WSGI_APPLICATION = 'dsbd.wsgi.application'

# Channels
ASGI_APPLICATION = 'dsbd.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get('DATABASE_NAME', 'dsbd'),
        "USER": os.environ.get('DATABASE_USER', 'dsbd'),
        "PASSWORD": os.environ.get('DATABASE_PASSWORD', ''),
        "HOST": os.environ.get('DATABASE_HOST', 'localhost'),
        "PORT": os.environ.get('DATABASE_PORT', 3306),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

# E-Mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'false').lower() == 'true'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Channel
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH_USER_MODEL
AUTH_USER_MODEL = 'custom_auth.User'

# DJANGO_TOOLBAR
if DEBUG:
    import os
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1"]

    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

LOGIN_URL = "sign_in"
LOGIN_REDIRECT_URL = "/"

DOMAIN_URL = os.environ.get('DOMAIN_URL', 'http://localhost:8000')

USER_LOGIN_VERIFY_EMAIL_EXPIRED_HOURS = os.environ.get('USER_LOGIN_VERIFY_EMAIL_EXPIRED_HOURS', 1)
USER_LOGIN_VERIFY_EMAIL_EXPIRED_MINUTES = os.environ.get('USER_LOGIN_VERIFY_EMAIL_EXPIRED_MINUTES', 10)
USER_ACTIVATE_EXPIRED_DAYS = os.environ.get('USER_ACTIVATE_EXPIRED_DAYS', 7)
SIGN_UP_EXPIRED_DAYS = os.environ.get('SIGN_UP_EXPIRED_DAYS', 7)

## Stripe
STRIPE_PRIVATE_KEY = os.environ.get('STRIPE_PRIVATE_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET_KEY = os.environ.get('STRIPE_WEBHOOK_SECRET_KEY', '')

## Slack
SLACK_WEBHOOK_LOG = os.environ.get('SLACK_WEBHOOK_LOG', '')

TWO_FACTOR_WEBAUTHN_RP_NAME = 'doornoc_dsbd'

## LDAP
AUTH_LDAP_SERVER_URI = os.environ.get('AUTH_LDAP_SERVER_URI', '')
AUTH_LDAP_BIND_DN = os.environ.get('AUTH_LDAP_BIND_DN', '')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('AUTH_LDAP_BIND_PASSWORD', '')
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    os.environ.get('AUTH_LDAP_USER_SEARCH_BASE_DN', ''),
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)"
)

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": os.environ.get('AUTH_LDAP_ATTR_FIRSTNAME', 'givenName'),
    "last_name": os.environ.get('AUTH_LDAP_ATTR_LASTNAME', 'sn'),
    "email": os.environ.get('AUTH_LDAP_ATTR_MAIL', 'mail'),
}
AUTH_LDAP_GROUP_TYPE = _import_ldap_group_type(os.environ.get('AUTH_LDAP_GROUP_TYPE', 'PosixGroupType'))

AUTH_LDAP_REQUIRE_GROUP_DN = os.environ.get('AUTH_LDAP_REQUIRE_GROUP_DN')

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    os.environ.get('AUTH_LDAP_GROUP_SEARCH_BASE_DN', ''),
    ldap.SCOPE_SUBTREE,
    "(objectClass=posixGroup)",
)

AUTH_LDAP_FIND_GROUP_PERMS = True

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": os.environ.get('AUTH_LDAP_REQUIRE_GROUP_DN', ''),
    "is_staff": os.environ.get('AUTH_LDAP_IS_ADMIN_DN', ''),
}
