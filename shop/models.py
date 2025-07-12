from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Product(models.Model):
    """商品模型（占位）"""
    name = models.CharField(_('商品名称'), max_length=200)
    description = models.TextField(_('商品描述'), blank=True)
    price = models.DecimalField(_('价格'), max_digits=10, decimal_places=2)
    image = models.ImageField(_('商品图片'), upload_to='shop/products/', blank=True, null=True)
    is_active = models.BooleanField(_('是否上架'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品')

    def __str__(self):
        return self.name