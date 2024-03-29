from django.contrib import admin

from dsbd.ticket.models import Template, Chat, Ticket


@admin.register(Ticket)
class Ticket(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("created_at", "updated_at", "user", "group")}),
        ('info', {'fields': ('template', 'title', 'body')}),
        ('Flags', {'fields': ('from_admin', 'is_solved', 'is_approve', 'is_reject')}),
    )
    list_display = (
        "id", "created_at", "updated_at", "user", "group", 'template', 'title', "is_solved",)
    list_filter = ("is_solved",)
    search_fields = ('user', 'group', 'from_admin', 'is_solved', 'is_approve', 'is_reject')


@admin.register(Template)
class Template(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at']
    fieldsets = (
        (None, {"fields": ("id", "number", "created_at", "is_active", 'comment')}),
        ('info', {'fields': ('type1', 'type2', 'title', 'body')}),
    )
    list_display = (
        "number", "created_at", "is_active", "type1", 'type2', 'title')
    list_filter = ("is_active",)
    search_fields = ("is_active", "type1', 'type2', 'title")
    ordering = ['number']


@admin.register(Chat)
class Chat(admin.ModelAdmin):
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {"fields": ("created_at", "user", "group", "ticket")}),
        ('info', {'fields': ('body',)}),
        ('Flags', {'fields': ('is_admin',)}),
    )
    list_display = (
        "id", "created_at", "user", "group", "ticket", "is_admin")
    list_filter = ("group",)
    search_fields = ("created_at", "user", "group", "ticket")
