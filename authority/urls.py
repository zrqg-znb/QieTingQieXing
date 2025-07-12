from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, RoleViewSet, MenuViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'menus', MenuViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]