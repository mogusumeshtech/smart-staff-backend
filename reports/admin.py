from django.contrib import admin
from reports.models import Report, DashboardMetric, AuditLog

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'generated_date', 'generated_by', 'format_type')
    list_filter = ('report_type', 'format_type', 'generated_date')
    search_fields = ('name', 'generated_by')
    readonly_fields = ('generated_date',)

@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_type', 'calculated_date', 'period_month', 'period_year')
    list_filter = ('metric_type', 'period_year', 'period_month')
    readonly_fields = ('calculated_date',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'object_id', 'action', 'performed_by', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('model_name', 'object_id', 'performed_by')
    readonly_fields = ('timestamp',)
