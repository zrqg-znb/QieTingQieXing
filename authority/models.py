from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    """用户角色模型"""
    name = models.CharField(_('角色名称'), max_length=50, unique=True)
    description = models.TextField(_('角色描述'), blank=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('权限'),
        blank=True,
    )
    is_active = models.BooleanField(_('是否激活'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('角色')
        verbose_name_plural = _('角色')

    def __str__(self):
        return self.name


class User(AbstractUser):
    """自定义用户模型"""
    nickname = models.CharField(_('昵称'), max_length=50, blank=True)
    avatar = models.ImageField(_('头像'), upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(_('手机号'), max_length=20, blank=True)
    bio = models.TextField(_('个人简介'), blank=True)
    roles = models.ManyToManyField(
        Role,
        verbose_name=_('角色'),
        blank=True,
        related_name='users'
    )
    is_deleted = models.BooleanField(_('是否删除'), default=False)
    last_login_ip = models.GenericIPAddressField(_('最后登录IP'), blank=True, null=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        """返回用户全名"""
        if self.first_name and self.last_name:
            return f'{self.last_name}{self.first_name}'
        return self.nickname or self.username


class Menu(models.Model):
    """菜单模型，用于前端动态菜单"""
    name = models.CharField(_('菜单名称'), max_length=50)
    parent = models.ForeignKey('self', verbose_name=_('父菜单'), on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    path = models.CharField(_('路由路径'), max_length=100)
    component = models.CharField(_('组件路径'), max_length=100, blank=True)
    icon = models.CharField(_('图标'), max_length=50, blank=True)
    sort_order = models.IntegerField(_('排序'), default=0)
    is_visible = models.BooleanField(_('是否可见'), default=True)
    roles = models.ManyToManyField(
        Role,
        verbose_name=_('可访问角色'),
        blank=True,
        related_name='menus'
    )
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('菜单')
        verbose_name_plural = _('菜单')
        ordering = ['sort_order']

    def __str__(self):
        return self.name