from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, Menu
from .serializers import (
    UserSerializer, UserCreateSerializer, UserLoginSerializer,
    PasswordChangeSerializer, UserProfileUpdateSerializer,
    RoleSerializer, MenuSerializer
)

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    """仅管理员可访问"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        elif self.action == 'update_profile':
            return UserProfileUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [permissions.AllowAny()]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            # 更新最后登录IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            user.last_login_ip = ip
            user.save(update_fields=['last_login_ip'])

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'detail': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """用户登出"""
        # JWT无状态，前端删除token即可，这里仅作为接口占位
        return Response({'detail': '登出成功'})

    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """修改密码"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        # 检查旧密码
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': '旧密码不正确'}, status=status.HTTP_400_BAD_REQUEST)

        # 设置新密码
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': '密码修改成功'})

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """更新个人资料"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    """角色视图集"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]


class MenuViewSet(viewsets.ModelViewSet):
    """菜单视图集"""
    queryset = Menu.objects.filter(parent=None).order_by('sort_order')
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def user_menus(self, request):
        """获取当前用户可访问的菜单"""
        user = request.user
        if user.is_superuser:
            # 超级管理员可以访问所有菜单
            menus = Menu.objects.filter(parent=None, is_visible=True).order_by('sort_order')
        else:
            # 普通用户根据角色获取菜单
            user_roles = user.roles.all()
            menus = Menu.objects.filter(
                parent=None,
                is_visible=True,
                roles__in=user_roles
            ).distinct().order_by('sort_order')

        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)