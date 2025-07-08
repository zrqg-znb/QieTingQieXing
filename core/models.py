from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """自定义用户模型"""
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

class Role(models.Model):
    """角色模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(null=True, blank=True, verbose_name='角色描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

class Permission(models.Model):
    """权限模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='权限名称')
    codename = models.CharField(max_length=100, unique=True, verbose_name='权限代码')
    description = models.TextField(null=True, blank=True, verbose_name='权限描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

class UserRole(models.Model):
    """用户角色关联模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles', verbose_name='用户')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users', verbose_name='角色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户角色'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'role']

    def __str__(self):
        return f'{self.user.username} - {self.role.name}'

class RolePermission(models.Model):
    """角色权限关联模型"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions', verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_roles', verbose_name='权限')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '角色权限'
        verbose_name_plural = verbose_name
        unique_together = ['role', 'permission']

    def __str__(self):
        return f'{self.role.name} - {self.permission.name}'

class SystemConfig(models.Model):
    """系统配置模型"""
    key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    value = models.TextField(verbose_name='配置值')
    description = models.TextField(null=True, blank=True, verbose_name='配置描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
        ordering = ['key']

    def __str__(self):
        return self.key
