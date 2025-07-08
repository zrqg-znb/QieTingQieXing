from rest_framework import serializers
from django.db.models import Count
from .models import DataSource, Chart, Dashboard, DashboardChart
from core.serializers import UserSerializer

class DataSourceListSerializer(serializers.ModelSerializer):
    """数据源列表序列化器"""
    created_by = UserSerializer(read_only=True)
    charts_count = serializers.SerializerMethodField()

    class Meta:
        model = DataSource
        fields = ['id', 'name', 'type', 'description', 'is_active',
                 'created_by', 'charts_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_charts_count(self, obj):
        return obj.charts.count()

class DataSourceDetailSerializer(serializers.ModelSerializer):
    """数据源详情序列化器"""
    created_by = UserSerializer(read_only=True)
    charts_count = serializers.SerializerMethodField()

    class Meta:
        model = DataSource
        fields = ['id', 'name', 'type', 'description', 'connection_details',
                 'is_active', 'created_by', 'charts_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'connection_details': {'write_only': True}
        }

    def get_charts_count(self, obj):
        return obj.charts.count()

class ChartListSerializer(serializers.ModelSerializer):
    """图表列表序列化器"""
    created_by = UserSerializer(read_only=True)
    data_source = DataSourceListSerializer(read_only=True)
    dashboards_count = serializers.SerializerMethodField()

    class Meta:
        model = Chart
        fields = ['id', 'name', 'type', 'description', 'data_source',
                 'refresh_interval', 'is_public', 'created_by',
                 'dashboards_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_dashboards_count(self, obj):
        return obj.chart_dashboards.count()

class ChartDetailSerializer(serializers.ModelSerializer):
    """图表详情序列化器"""
    created_by = UserSerializer(read_only=True)
    data_source = DataSourceListSerializer(read_only=True)
    data_source_id = serializers.IntegerField(write_only=True)
    dashboards = serializers.SerializerMethodField()

    class Meta:
        model = Chart
        fields = ['id', 'name', 'type', 'description', 'data_source',
                 'data_source_id', 'query', 'config', 'refresh_interval',
                 'is_public', 'created_by', 'dashboards', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_dashboards(self, obj):
        dashboard_charts = obj.chart_dashboards.select_related('dashboard')
        return [{
            'id': dc.dashboard.id,
            'name': dc.dashboard.name,
            'position': dc.position
        } for dc in dashboard_charts]

class DashboardChartSerializer(serializers.ModelSerializer):
    """仪表盘图表关联序列化器"""
    chart = ChartListSerializer(read_only=True)
    chart_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = DashboardChart
        fields = ['id', 'dashboard', 'chart', 'chart_id', 'position']
        read_only_fields = ['created_at']

class DashboardListSerializer(serializers.ModelSerializer):
    """仪表盘列表序列化器"""
    created_by = UserSerializer(read_only=True)
    charts_count = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = ['id', 'name', 'description', 'is_public',
                 'created_by', 'charts_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_charts_count(self, obj):
        return obj.dashboard_charts.count()

class DashboardDetailSerializer(serializers.ModelSerializer):
    """仪表盘详情序列化器"""
    created_by = UserSerializer(read_only=True)
    charts = DashboardChartSerializer(source='dashboard_charts', many=True, read_only=True)
    chart_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Dashboard
        fields = ['id', 'name', 'description', 'layout', 'charts', 'chart_ids',
                 'is_public', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        chart_ids = validated_data.pop('chart_ids', [])
        dashboard = Dashboard.objects.create(**validated_data)
        for chart_id in chart_ids:
            DashboardChart.objects.create(
                dashboard=dashboard,
                chart_id=chart_id,
                position={'x': 0, 'y': 0}
            )
        return dashboard

    def update(self, instance, validated_data):
        chart_ids = validated_data.pop('chart_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if chart_ids is not None:
            instance.dashboard_charts.all().delete()
            for chart_id in chart_ids:
                DashboardChart.objects.create(
                    dashboard=instance,
                    chart_id=chart_id,
                    position={'x': 0, 'y': 0}
                )
        return instance