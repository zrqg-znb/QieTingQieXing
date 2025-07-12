from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TagViewSet, ArticleViewSet, CommentViewSet, AttachmentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'attachments', AttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]