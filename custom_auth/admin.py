from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from custom_auth.models import CustomGroup, User


@admin.register(CustomGroup)
class AdminGroup(GroupAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(User)
class AdminUser(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'groups')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_member', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')
