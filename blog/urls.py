from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)
router.register('articles', views.ArticleViewSet)
router.register('comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]