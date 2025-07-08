from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Count, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Category, Tag, Article, Comment
from .serializers import (
    CategorySerializer, TagSerializer,
    ArticleListSerializer, ArticleDetailSerializer,
    CommentSerializer, CommentReplySerializer
)

class IsAuthorOrReadOnly(permissions.BasePermission):
    """作者可以修改，其他人只读的权限类"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        category = self.get_object()
        articles = category.articles.filter(is_published=True)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    """标签视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        tag = self.get_object()
        articles = tag.articles.filter(is_published=True)
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleViewSet(viewsets.ModelViewSet):
    """文章视图集"""
    queryset = Article.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'summary']
    ordering_fields = ['created_at', 'updated_at', 'views_count', 'likes_count']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.action == 'list':
                return Article.objects.filter(
                    Q(is_published=True) | Q(author=self.request.user)
                )
            return Article.objects.all()
        return Article.objects.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_published', False):
            serializer.validated_data['published_at'] = timezone.now()
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if not instance.is_published and serializer.validated_data.get('is_published', False):
            serializer.validated_data['published_at'] = timezone.now()
        serializer.save()

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        article = self.get_object()
        article.likes_count = F('likes_count') + 1
        article.save()
        article.refresh_from_db()
        return Response({'likes_count': article.likes_count})

    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        article = self.get_object()
        article.views_count = F('views_count') + 1
        article.save()
        article.refresh_from_db()
        return Response({'views_count': article.views_count})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        article = self.get_object()
        comments = article.comments.filter(
            parent_comment__isnull=True,
            is_active=True
        ).order_by('-created_at')
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """评论视图集"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'likes_count']

    def get_queryset(self):
        queryset = Comment.objects.filter(is_active=True)
        article_id = self.request.query_params.get('article')
        parent_id = self.request.query_params.get('parent')
        if article_id:
            queryset = queryset.filter(article_id=article_id)
        if parent_id:
            queryset = queryset.filter(parent_comment_id=parent_id)
        else:
            queryset = queryset.filter(parent_comment__isnull=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create' and self.request.data.get('parent_comment'):
            return CommentReplySerializer
        return CommentSerializer

    def perform_create(self, serializer):
        article_id = self.request.data.get('article')
        article = get_object_or_404(Article, id=article_id)
        serializer.save(author=self.request.user, article=article)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        comment.likes_count = F('likes_count') + 1
        comment.save()
        comment.refresh_from_db()
        return Response({'likes_count': comment.likes_count})

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        comment = self.get_object()
        replies = comment.replies.filter(is_active=True).order_by('created_at')
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = CommentReplySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentReplySerializer(replies, many=True)
        return Response(serializer.data)
