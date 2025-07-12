from rest_framework import viewsets, permissions, filters
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """商品视图集（占位）"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]