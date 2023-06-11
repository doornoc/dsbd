from django.contrib import admin

from .models import Service


@admin.register(Service)
class Service(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("created_at", "start_at", "end_at", "group", "is_active")}),
        ('info', {'fields': ('type1', 'content')}),
    )
    list_display = (
        "id", "group", "created_at", "start_at", "end_at", "type1", "is_active",)
    list_filter = ("end_at",)
    search_fields = ("end_at", "group", "type1", "is_active")
