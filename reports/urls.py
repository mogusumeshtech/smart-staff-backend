from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reports.views import ReportViewSet, DashboardMetricViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'metrics', DashboardMetricViewSet, basename='dashboard-metric')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
]
