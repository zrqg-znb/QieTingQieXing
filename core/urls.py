from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authority.urls')),  # 用户认证相关路由
    path('api/wiki/', include('wiki.urls')),      # 知识库相关路由
    path('api/shop/', include('shop.urls')),      # 商城相关路由（占位）
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)