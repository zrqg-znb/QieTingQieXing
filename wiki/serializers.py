from rest_framework import serializers
from .models import Category, Tag, Article, Comment, Attachment
from django.contrib.auth import get_user_model

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    """用户简要信息序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar']


class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'sort_order', 'is_active', 'children']

    def get_children(self, obj):
        """获取子分类"""
        children = Category.objects.filter(parent=obj).order_by('sort_order')
        serializer = CategorySerializer(children, many=True)
        return serializer.data


class AttachmentSerializer(serializers.ModelSerializer):
    """附件序列化器"""
    class Meta:
        model = Attachment
        fields = ['id', 'name', 'file', 'file_size', 'download_count', 'created_at']
        read_only_fields = ['file_size', 'download_count']


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    user = UserBriefSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'parent', 'content', 'is_active', 'created_at', 'replies']
        read_only_fields = ['user', 'is_active']

    def get_replies(self, obj):
        """获取回复"""
        replies = Comment.objects.filter(parent=obj, is_active=True)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

    def create(self, validated_data):
        """创建评论"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    author = UserBriefSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'summary', 'category', 'category_name', 'author', 
                  'tags', 'status', 'is_pinned', 'view_count', 'like_count', 
                  'created_at', 'published_at']
        read_only_fields = ['view_count', 'like_count']


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        write_only=True,
        source='category'
    )
    author = UserBriefSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        write_only=True,
        many=True,
        required=False,
        source='tags'
    )
    attachments = AttachmentSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'summary', 'category', 'category_id', 
                  'author', 'tags', 'tag_ids', 'status', 'is_pinned', 'view_count', 
                  'like_count', 'created_at', 'updated_at', 'published_at', 
                  'attachments', 'comments']
        read_only_fields = ['author', 'view_count', 'like_count', 'created_at', 'updated_at', 'published_at']

    def get_comments(self, obj):
        """获取评论"""
        # 只获取顶级评论，回复通过CommentSerializer的get_replies方法获取
        comments = Comment.objects.filter(article=obj, parent=None, is_active=True)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def create(self, validated_data):
        """创建文章"""
        tags_data = validated_data.pop('tags', [])
        validated_data['author'] = self.context['request'].user
        article = super().create(validated_data)
        article.tags.set(tags_data)
        return article

    def update(self, instance, validated_data):
        """更新文章"""
        tags_data = validated_data.pop('tags', None)
        article = super().update(instance, validated_data)
        if tags_data is not None:
            article.tags.set(tags_data)
        return article