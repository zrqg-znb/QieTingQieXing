from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('data-sources', views.DataSourceViewSet)
router.register('charts', views.ChartViewSet)
router.register('dashboards', views.DashboardViewSet)
router.register('dashboard-charts', views.DashboardChartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]