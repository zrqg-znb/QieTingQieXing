from rest_framework import serializers
from django.utils import timezone
from .models import Category, Tag, Article, Comment
from core.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    articles_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'articles_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_articles_count(self, obj):
        return obj.articles.filter(is_published=True).count()

class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    articles_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'articles_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_articles_count(self, obj):
        return obj.articles.filter(is_published=True).count()

class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'summary', 'author', 'category',
                 'tags', 'cover_image', 'views_count', 'likes_count',
                 'comments_count', 'is_published', 'published_at',
                 'created_at', 'updated_at']
        read_only_fields = ['slug', 'views_count', 'likes_count',
                          'comments_count', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.filter(is_active=True).count()

class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'slug', 'author', 'category',
                 'category_id', 'tags', 'tag_ids', 'cover_image', 'summary',
                 'is_published', 'views_count', 'likes_count', 'comments_count',
                 'published_at', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'views_count', 'likes_count',
                          'comments_count', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.filter(is_active=True).count()

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        if validated_data.get('is_published', False):
            validated_data['published_at'] = timezone.now()
        article = Article.objects.create(**validated_data)
        if tag_ids:
            article.tags.set(tag_ids)
        return article

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        if not instance.is_published and validated_data.get('is_published', False):
            validated_data['published_at'] = timezone.now()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance

class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'content', 'parent_comment',
                 'replies', 'likes_count', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['replies', 'likes_count', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.parent_comment is None:  # 只获取直接回复
            replies = obj.replies.filter(is_active=True).order_by('created_at')
            return CommentReplySerializer(replies, many=True).data
        return []

class CommentReplySerializer(serializers.ModelSerializer):
    """评论回复序列化器"""
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'likes_count',
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['likes_count', 'created_at', 'updated_at']