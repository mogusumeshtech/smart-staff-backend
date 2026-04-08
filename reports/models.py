from django.db import models
from core.models import BaseModel

class Report(BaseModel):
    REPORT_TYPES = (
        ('staff_summary', 'Staff Summary Report'),
        ('payroll_summary', 'Payroll Summary Report'),
        ('salary_advance_summary', 'Salary Advance Summary'),
        ('department_analysis', 'Department Analysis'),
        ('category_analysis', 'Category Analysis'),
        ('attendance_analysis', 'Attendance Analysis'),
        ('tax_report', 'Tax Report'),
        ('bank_advise', 'Bank Advise'),
    )
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    generated_date = models.DateTimeField(auto_now_add=True)
    generated_by = models.CharField(max_length=100, blank=True, null=True)
    period_from = models.DateField(blank=True, null=True)
    period_to = models.DateField(blank=True, null=True)
    
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    format_type = models.CharField(
        max_length=10,
        choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')],
        default='pdf'
    )
    
    filters = models.JSONField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-generated_date']
    
    def __str__(self):
        return self.name


class DashboardMetric(BaseModel):
    METRIC_TYPES = (
        ('total_staff', 'Total Staff'),
        ('total_payroll', 'Total Payroll'),
        ('pending_advances', 'Pending Salary Advances'),
        ('department_count', 'Department Count'),
        ('active_staff', 'Active Staff'),
        ('teaching_vs_nonteaching', 'Teaching vs Non-Teaching'),
        ('average_salary', 'Average Salary'),
        ('gender_distribution', 'Gender Distribution'),
    )
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.JSONField()
    calculated_date = models.DateTimeField(auto_now_add=True)
    period_month = models.IntegerField(blank=True, null=True)
    period_year = models.IntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Dashboard Metric'
        verbose_name_plural = 'Dashboard Metrics'
        ordering = ['-calculated_date']
    
    def __str__(self):
        return f"{self.get_metric_type_display()}"


class AuditLog(BaseModel):
    ACTION_CHOICES = (
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('download', 'Downloaded'),
    )
    
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    performed_by = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model_name', 'object_id']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.model_name} - {self.action} - {self.timestamp}"
