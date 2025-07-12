from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F
from .models import Category, Tag, Article, Comment, Attachment
from .serializers import (
    CategorySerializer, TagSerializer, ArticleListSerializer, 
    ArticleDetailSerializer, CommentSerializer, AttachmentSerializer
)
from authority.permissions import IsOwnerOrAdmin, HasRolePermission


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.filter(parent=None).order_by('sort_order')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [HasRolePermission(['admin', 'editor'])()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def all(self, request):
        """获取所有分类（包括子分类）"""
        categories = Category.objects.filter(is_active=True).order_by('sort_order')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """标签视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [HasRolePermission(['admin', 'editor'])()]
        return [permissions.IsAuthenticated()]


class ArticleViewSet(viewsets.ModelViewSet):
    """文章视图集"""
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'summary']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """根据不同条件获取文章列表"""
        queryset = Article.objects.all()
        
        # 根据状态筛选
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        else:
            # 默认只显示已发布的文章
            queryset = queryset.filter(status='published')
        
        # 根据分类筛选
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 根据标签筛选
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        
        # 根据作者筛选
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # 我的文章
        if self.action == 'my_articles':
            queryset = queryset.filter(author=self.request.user)
        
        # 置顶文章优先
        queryset = queryset.order_by('-is_pinned', '-created_at')
        
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """获取文章详情，并增加浏览次数"""
        instance = self.get_object()
        # 增加浏览次数
        instance.view_count = F('view_count') + 1
        instance.save(update_fields=['view_count'])
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞文章"""
        article = self.get_object()
        article.like_count = F('like_count') + 1
        article.save(update_fields=['like_count'])
        article.refresh_from_db()
        return Response({'like_count': article.like_count})

    @action(detail=False, methods=['get'])
    def my_articles(self, request):
        """获取我的文章"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticleListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布文章"""
        article = self.get_object()
        if article.status == 'published':
            return Response({'detail': '文章已经是发布状态'}, status=status.HTTP_400_BAD_REQUEST)
        
        article.status = 'published'
        article.published_at = timezone.now()
        article.save(update_fields=['status', 'published_at'])
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """归档文章"""
        article = self.get_object()
        article.status = 'archived'
        article.save(update_fields=['status'])
        serializer = self.get_serializer(article)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """评论视图集"""
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """根据文章ID获取评论"""
        queryset = Comment.objects.filter(is_active=True)
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article_id=article_id, parent=None)
        return queryset.order_by('-created_at')

    def perform_destroy(self, instance):
        """软删除评论"""
        instance.is_active = False
        instance.save(update_fields=['is_active'])


class AttachmentViewSet(viewsets.ModelViewSet):
    """附件视图集"""
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """根据文章ID获取附件"""
        queryset = Attachment.objects.all()
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article_id=article_id)
        return queryset

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """下载附件并增加下载次数"""
        attachment = self.get_object()
        attachment.download_count = F('download_count') + 1
        attachment.save(update_fields=['download_count'])
        # 实际下载逻辑在前端处理，这里只增加下载次数
        return Response({'detail': '下载次数已增加'})