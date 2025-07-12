from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Role, Menu


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'nickname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'roles')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('个人信息'), {'fields': ('nickname', 'first_name', 'last_name', 'email', 'avatar', 'phone', 'bio')}),
        (_('权限'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'roles', 'groups', 'user_permissions')}),
        (_('重要日期'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('roles', 'groups', 'user_permissions')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    filter_horizontal = ('permissions',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'path', 'component', 'sort_order', 'is_visible')
    list_filter = ('is_visible', 'parent')
    search_fields = ('name', 'path', 'component')
    list_editable = ('sort_order', 'is_visible')
    filter_horizontal = ('roles',)