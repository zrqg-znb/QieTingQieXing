from django.db import models
from core.models import User

class DataSource(models.Model):
    """数据源模型"""
    TYPE_CHOICES = [
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL'),
        ('csv', 'CSV文件'),
        ('api', 'API接口'),
    ]

    name = models.CharField(max_length=100, verbose_name='数据源名称')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='数据源类型')
    connection_details = models.JSONField(verbose_name='连接信息')
    description = models.TextField(null=True, blank=True, verbose_name='数据源描述')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_sources', verbose_name='创建者')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '数据源'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Chart(models.Model):
    """图表模型"""
    TYPE_CHOICES = [
        ('line', '折线图'),
        ('bar', '柱状图'),
        ('pie', '饼图'),
        ('scatter', '散点图'),
        ('area', '面积图'),
        ('radar', '雷达图'),
        ('gauge', '仪表盘'),
        ('funnel', '漏斗图'),
    ]

    name = models.CharField(max_length=100, verbose_name='图表名称')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='图表类型')
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='charts', verbose_name='数据源')
    config = models.JSONField(verbose_name='图表配置')
    query = models.TextField(verbose_name='数据查询语句')
    refresh_interval = models.PositiveIntegerField(default=0, verbose_name='刷新间隔(秒)')
    description = models.TextField(null=True, blank=True, verbose_name='图表描述')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='charts', verbose_name='创建者')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '图表'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Dashboard(models.Model):
    """仪表盘模型"""
    name = models.CharField(max_length=100, verbose_name='仪表盘名称')
    description = models.TextField(null=True, blank=True, verbose_name='仪表盘描述')
    layout = models.JSONField(default=dict, verbose_name='布局配置')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards', verbose_name='创建者')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '仪表盘'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class DashboardChart(models.Model):
    """仪表盘图表关联模型"""
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='dashboard_charts', verbose_name='仪表盘')
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, related_name='chart_dashboards', verbose_name='图表')
    position = models.JSONField(verbose_name='位置信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '仪表盘图表'
        verbose_name_plural = verbose_name
        unique_together = ['dashboard', 'chart']
        ordering = ['dashboard', 'chart']

    def __str__(self):
        return f'{self.dashboard.name} - {self.chart.name}'
