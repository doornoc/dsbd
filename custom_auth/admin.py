from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from custom_auth.models import Group, User, SignUpKey, UserActivateToken, UserGroup


class TermInlineUserAdmin(admin.TabularInline):
    model = User.groups.through
    extra = 1


@admin.register(User)
class AdminUser(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',)}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
        ('Options', {'fields': ('add_group',)}),
        ('Charge', {'fields': ('is_charge', 'expired_at', 'stripe_customer_id', 'stripe_subscription_id')}),
    )
    list_display = ('username', 'email', 'is_staff',)
    list_filter = ("is_staff", "is_active",)
    search_fields = ('username', 'email')
    filter_horizontal = ('groups',)

    inlines = (TermInlineUserAdmin,)

    def get_groups(self, obj):
        return "\n".join([p.groups for p in obj.group.all()])


@admin.register(Group)
class AdminGroup(ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', "is_active", "comment")}),
        ('Personal info', {'fields': ('zipcode', 'address', 'address_en', 'email', 'phone')}),
        ('Important dates', {'fields': ('created_at',)}),
        ('Charge', {'fields': ('is_charge', 'expired_at', 'stripe_customer_id', 'stripe_subscription_id')}),
    )
    list_display = ('name', "is_active", "comment")
    search_fields = ('name', "is_active", "comment")


@admin.register(UserGroup)
class AdminUserGroup(ModelAdmin):
    fieldsets = (
        (None, {'fields': ('created_at', 'user', "group")}),
        ('Option', {'fields': ('is_admin',)}),
        ('LDAP', {'fields': ('ldap_register', 'enable_ldap')}),
    )
    list_display = ('user', "group", "is_admin")
    search_fields = ('user', "group", "is_admin")


@admin.register(SignUpKey)
class AdminSignUpKey(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("key", "comment", "expired_at", 'is_used')}),
        ('Important dates', {'fields': ('created_at',)}),
    )
    list_display = ('key', 'comment', 'expired_at', 'is_used')
    search_fields = ('key', 'expired_at', 'is_used')


@admin.register(UserActivateToken)
class AdminUserActivateToken(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "token", "expired_at", "is_used")}),
        ('Important dates', {'fields': ('created_at',)}),
    )
    list_display = ('user', 'token', 'expired_at', 'is_used')
    search_fields = ('user', 'token', 'expired_at', 'is_used')
