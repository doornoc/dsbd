"""
URL configuration for dsbd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from dsbd import views
from custom_auth import views as custom_auth_views


urlpatterns = [
    path("", views.index, name="index"),
    path("payment/", views.payment, name="payment"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path('forget/', views.PasswordReset.as_view(), name='password_reset'),
    path('forget/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('forget/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('forget/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('activate/<uuid:activate_token>/', views.activate_user, name='activate_user'),
    path("service/", include("dsbd.service.urls")),
    path("ticket/", include("dsbd.ticket.urls")),
    path("profile/", include("custom_auth.urls")),
    path("stripe_webhook/", views.stripe_webhook, name="webhook"),
    path("group/", custom_auth_views.get_groups, name="get_groups"),
    path("group/add/", custom_auth_views.group_add, name="add_group"),
    path("group/edit/<int:group_id>", custom_auth_views.group_edit, name="edit_group"),
    path("group/permission/<int:group_id>", custom_auth_views.group_permission, name="permission_group"),
    path("group/<int:group_id>/payment", custom_auth_views.group_payment, name="group_payment"),
    path('admin/custom/', include("dsbd.custom_admin.urls")),
    path('admin/login/', views.admin_sign_in, name='admin_sign_in'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
