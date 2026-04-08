from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from reports.models import Report, DashboardMetric, AuditLog
from reports.serializers import ReportSerializer, DashboardMetricSerializer, AuditLogSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'format_type']
    search_fields = ['name', 'generated_by']
    ordering_fields = ['generated_date', 'name']
    ordering = ['-generated_date']

class DashboardMetricViewSet(viewsets.ModelViewSet):
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['metric_type', 'period_year', 'period_month']

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name']
    search_fields = ['performed_by', 'object_id']
    ordering_fields = ['timestamp', 'action']
    ordering = ['-timestamp']
