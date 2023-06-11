from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from custom_auth.models import CustomGroup, User, SignUpKey, UserActivateToken


@admin.register(User)
class AdminUser(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'groups')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_member', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(SignUpKey)
class AdminSignUpKey(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("key", "comment", "expired_at", 'is_used')}),
    )
    list_display = ('key', 'comment', 'expired_at', 'is_used')
    search_fields = ('key', 'expired_at', 'is_used')


@admin.register(UserActivateToken)
class AdminUserActivateToken(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "token", "expired_at", "is_used")}),
    )
    list_display = ('user', 'token', 'expired_at', 'is_used')
    search_fields = ('user', 'token', 'expired_at', 'is_used')


@admin.register(CustomGroup)
class AdminGroup(GroupAdmin):
    fieldsets = (
        (None, {'fields': ('name', "is_active", "admin_user", "comment")}),
    )
    list_display = ('name', "is_active", "comment")
    search_fields = ('name', "is_active", "comment")
