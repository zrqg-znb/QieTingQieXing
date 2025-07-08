from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connections
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
import requests
import pandas as pd
from .models import DataSource, Chart, Dashboard, DashboardChart
from .serializers import (
    DataSourceListSerializer, DataSourceDetailSerializer,
    ChartListSerializer, ChartDetailSerializer,
    DashboardListSerializer, DashboardDetailSerializer,
    DashboardChartSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """创建者可以修改，其他人只读的权限类"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class DataSourceViewSet(viewsets.ModelViewSet):
    """数据源视图集"""
    queryset = DataSource.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'type', 'description']
    ordering_fields = ['created_at', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return DataSourceListSerializer
        return DataSourceDetailSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return DataSource.objects.all()
        return DataSource.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        data_source = self.get_object()
        try:
            if data_source.type == 'mysql' or data_source.type == 'postgresql':
                conn_params = data_source.connection_details.copy()
                conn_params['alias'] = f'test_{data_source.id}'
                connections.create_connection(**conn_params)
                with connections[conn_params['alias']].cursor() as cursor:
                    cursor.execute('SELECT 1')
                return Response({'status': 'success', 'message': '连接成功'})
            elif data_source.type == 'api':
                api_url = data_source.connection_details.get('url')
                response = requests.get(api_url)
                response.raise_for_status()
                return Response({'status': 'success', 'message': '连接成功'})
            elif data_source.type == 'csv':
                file_path = data_source.connection_details.get('file_path')
                pd.read_csv(file_path)
                return Response({'status': 'success', 'message': '文件读取成功'})
            else:
                return Response(
                    {'error': '不支持的数据源类型'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'连接失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class ChartViewSet(viewsets.ModelViewSet):
    """图表视图集"""
    queryset = Chart.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'type']
    ordering_fields = ['created_at', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ChartListSerializer
        return ChartDetailSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Chart.objects.all()
        return Chart.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def preview_data(self, request, pk=None):
        chart = self.get_object()
        limit = request.data.get('limit', 100)
        try:
            if chart.data_source.type in ['mysql', 'postgresql']:
                with connections[f'test_{chart.data_source.id}'].cursor() as cursor:
                    cursor.execute(f"{chart.query} LIMIT {limit}")
                    columns = [col[0] for col in cursor.description]
                    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return Response({
                        'columns': columns,
                        'data': data,
                        'total': len(data)
                    })
            elif chart.data_source.type == 'api':
                api_url = chart.data_source.connection_details.get('url')
                response = requests.get(api_url)
                data = response.json()
                return Response({
                    'data': data[:limit],
                    'total': len(data)
                })
            elif chart.data_source.type == 'csv':
                file_path = chart.data_source.connection_details.get('file_path')
                df = pd.read_csv(file_path)
                data = df.head(limit).to_dict('records')
                return Response({
                    'columns': list(df.columns),
                    'data': data,
                    'total': len(df)
                })
            else:
                return Response(
                    {'error': '不支持的数据源类型'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'数据预览失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class DashboardViewSet(viewsets.ModelViewSet):
    """仪表盘视图集"""
    queryset = Dashboard.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def get_serializer_class(self):
        if self.action == 'list':
            return DashboardListSerializer
        return DashboardDetailSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Dashboard.objects.all()
        return Dashboard.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True)
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def update_layout(self, request, pk=None):
        dashboard = self.get_object()
        charts_layout = request.data.get('charts_layout', [])
        
        try:
            for layout in charts_layout:
                chart_id = layout.pop('chart_id')
                position = layout.get('position', {'x': 0, 'y': 0})
                DashboardChart.objects.filter(
                    dashboard=dashboard,
                    chart_id=chart_id
                ).update(position=position)
            
            return Response({'status': 'success', 'message': '布局更新成功'})
        except Exception as e:
            return Response(
                {'error': f'布局更新失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def refresh_data(self, request, pk=None):
        dashboard = self.get_object()
        charts_data = {}
        
        try:
            for dashboard_chart in dashboard.dashboard_charts.all():
                chart = dashboard_chart.chart
                if chart.data_source.type in ['mysql', 'postgresql']:
                    with connections[f'test_{chart.data_source.id}'].cursor() as cursor:
                        cursor.execute(chart.query)
                        columns = [col[0] for col in cursor.description]
                        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        charts_data[chart.id] = {
                            'columns': columns,
                            'data': data
                        }
                # 添加其他数据源类型的处理逻辑
            
            return Response(charts_data)
        except Exception as e:
            return Response(
                {'error': f'数据刷新失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class DashboardChartViewSet(viewsets.ModelViewSet):
    """仪表盘图表关联视图集"""
    queryset = DashboardChart.objects.all()
    serializer_class = DashboardChartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        dashboard_id = self.request.query_params.get('dashboard')
        if dashboard_id:
            return DashboardChart.objects.filter(dashboard_id=dashboard_id)
        return DashboardChart.objects.none()
