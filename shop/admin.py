from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """商品管理（占位）"""
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')