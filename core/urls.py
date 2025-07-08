from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('roles', views.RoleViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('user-roles', views.UserRoleViewSet)
router.register('role-permissions', views.RolePermissionViewSet)
router.register('system-config', views.SystemConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]