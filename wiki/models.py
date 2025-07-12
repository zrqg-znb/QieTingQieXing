from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Category(models.Model):
    """知识库分类"""
    name = models.CharField(_('分类名称'), max_length=100)
    description = models.TextField(_('分类描述'), blank=True)
    parent = models.ForeignKey('self', verbose_name=_('父分类'), on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.CharField(_('图标'), max_length=50, blank=True)
    sort_order = models.IntegerField(_('排序'), default=0)
    is_active = models.BooleanField(_('是否激活'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('分类')
        verbose_name_plural = _('分类')
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """知识库标签"""
    name = models.CharField(_('标签名称'), max_length=50, unique=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('标签')
        verbose_name_plural = _('标签')

    def __str__(self):
        return self.name


class Article(models.Model):
    """知识库文章"""
    STATUS_CHOICES = (
        ('draft', _('草稿')),
        ('published', _('已发布')),
        ('archived', _('已归档')),
    )
    
    title = models.CharField(_('标题'), max_length=200)
    content = models.TextField(_('内容'))
    summary = models.TextField(_('摘要'), blank=True)
    category = models.ForeignKey(Category, verbose_name=_('分类'), on_delete=models.CASCADE, related_name='articles')
    tags = models.ManyToManyField(Tag, verbose_name=_('标签'), blank=True, related_name='articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('作者'), on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='draft')
    is_pinned = models.BooleanField(_('是否置顶'), default=False)
    view_count = models.PositiveIntegerField(_('浏览次数'), default=0)
    like_count = models.PositiveIntegerField(_('点赞次数'), default=0)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    published_at = models.DateTimeField(_('发布时间'), null=True, blank=True)

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = _('文章')
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """文章评论"""
    article = models.ForeignKey(Article, verbose_name=_('文章'), on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('用户'), on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', verbose_name=_('父评论'), on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(_('评论内容'))
    is_active = models.BooleanField(_('是否激活'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('评论')
        verbose_name_plural = _('评论')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'


class Attachment(models.Model):
    """文章附件"""
    article = models.ForeignKey(Article, verbose_name=_('文章'), on_delete=models.CASCADE, related_name='attachments')
    name = models.CharField(_('附件名称'), max_length=100)
    file = models.FileField(_('附件文件'), upload_to='wiki/attachments/')
    file_size = models.PositiveIntegerField(_('文件大小'), default=0)  # 单位：字节
    download_count = models.PositiveIntegerField(_('下载次数'), default=0)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('附件')
        verbose_name_plural = _('附件')

    def __str__(self):
        return self.name