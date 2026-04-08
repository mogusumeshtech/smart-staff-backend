from rest_framework import serializers
from reports.models import Report, DashboardMetric, AuditLog

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id', 'name', 'report_type', 'description', 'generated_date', 'generated_by',
            'period_from', 'period_to', 'file_path', 'format_type', 'filters', 'is_active'
        )
        read_only_fields = ('id', 'generated_date', 'file_path')

class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = ('id', 'metric_type', 'value', 'calculated_date', 'period_month', 'period_year')
        read_only_fields = ('id', 'calculated_date')

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'model_name', 'object_id', 'action', 'performed_by', 'timestamp', 'changes', 'remarks')
        read_only_fields = ('id', 'timestamp')
