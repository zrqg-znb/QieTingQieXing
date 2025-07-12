from django.contrib import admin
from .models import Category, Tag, Article, Comment, Attachment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'description', 'sort_order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    list_editable = ('sort_order', 'is_active')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'is_pinned', 'view_count', 'created_at')
    list_filter = ('status', 'is_pinned', 'category', 'tags')
    search_fields = ('title', 'content', 'summary')
    list_editable = ('status', 'is_pinned')
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    readonly_fields = ('view_count', 'like_count')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'content', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'user__username', 'article__title')
    list_editable = ('is_active',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'file_size', 'download_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'article__title')
    readonly_fields = ('file_size', 'download_count')