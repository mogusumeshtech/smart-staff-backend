from django.contrib import admin
from salary_advances.models import SalaryAdvance, SalaryAdvanceRecovery

@admin.register(SalaryAdvance)
class SalaryAdvanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'amount', 'status', 'requested_date', 'approval_date')
    list_filter = ('status', 'requested_date', 'approval_date')
    search_fields = ('staff__first_name', 'staff__last_name', 'staff__email')
    readonly_fields = ('requested_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {'fields': ('staff', 'amount', 'reason', 'repayment_months')}),
        ('Status', {'fields': ('status', 'approved_by', 'remarks')}),
        ('Dates', {'fields': ('requested_date', 'approval_date', 'disbursal_date')}),
        ('Recovery', {'fields': ('amount_recovered',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'is_active')}),
    )

@admin.register(SalaryAdvanceRecovery)
class SalaryAdvanceRecoveryAdmin(admin.ModelAdmin):
    list_display = ('salary_advance', 'payroll_month', 'amount_recovered')
    list_filter = ('payroll_month', 'created_at')
    search_fields = ('salary_advance__staff__first_name', 'salary_advance__staff__last_name')
    readonly_fields = ('created_at', 'updated_at')
