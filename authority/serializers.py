from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Role, Menu

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'is_active']


class MenuSerializer(serializers.ModelSerializer):
    """菜单序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'path', 'component', 'icon', 'sort_order', 'is_visible', 'children']

    def get_children(self, obj):
        """获取子菜单"""
        children = Menu.objects.filter(parent=obj).order_by('sort_order')
        serializer = MenuSerializer(children, many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    roles = RoleSerializer(many=True, read_only=True)
    role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        write_only=True,
        many=True,
        required=False,
        source='roles'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'avatar', 'phone', 'bio', 
                  'is_active', 'date_joined', 'last_login', 'roles', 'role_ids']
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'nickname', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码不匹配"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    """密码修改序列化器"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "两次密码不匹配"})
        return attrs


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器"""
    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'phone', 'bio']