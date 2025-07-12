from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器（占位）"""
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'is_active', 'created_at']
        read_only_fields = ['created_at']