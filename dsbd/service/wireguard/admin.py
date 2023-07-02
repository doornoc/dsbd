from django.contrib import admin

from .models import Service, Server


@admin.register(Service)
class Service(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "is_active", "service")}),
        ('info', {'fields': ('ipv4', 'ipv6', 'server', "public_key",)}),
    )
    list_display = ("id", "service", "ipv4", "ipv6",)
    list_filter = ("is_active",)
    search_fields = ("is_active",)


@admin.register(Server)
class Server(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "is_active")}),
        ('Global', {'fields': ('start_ip', 'size', 'gateway_ip', 'global_ip', 'global_port', 'mgmt_ip', 'mgmt_port')}),
        ('key', {'fields': ('private_key', 'public_key')}),
    )
    list_display = ("id", "created_at", "is_active", "private_key", "public_key",)
    list_filter = ("is_active",)
    search_fields = ("is_active",)
