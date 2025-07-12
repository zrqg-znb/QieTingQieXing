from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """对象所有者或管理员权限"""
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问任何对象
        if request.user.is_staff:
            return True
            
        # 检查对象是否有user属性
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # 检查对象是否为User实例
        if hasattr(obj, 'username'):
            return obj == request.user
            
        return False


class HasRolePermission(permissions.BasePermission):
    """基于角色的权限控制"""
    
    def __init__(self, required_roles=None):
        self.required_roles = required_roles or []
    
    def has_permission(self, request, view):
        # 未登录用户没有权限
        if not request.user or not request.user.is_authenticated:
            return False
            
        # 超级管理员拥有所有权限
        if request.user.is_superuser:
            return True
            
        # 如果没有指定角色要求，则登录用户都有权限
        if not self.required_roles:
            return True
            
        # 检查用户是否拥有所需角色
        user_roles = request.user.roles.all()
        user_role_names = [role.name for role in user_roles]
        
        for role_name in self.required_roles:
            if role_name in user_role_names:
                return True
                
        return False