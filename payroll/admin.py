from django.contrib import admin
from payroll.models import PayrollPeriod, Payroll, PayrollEarning, PayrollDeduction

@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_date', 'end_date', 'status', 'processed_by')
    list_filter = ('status', 'year', 'month')
    readonly_fields = ('processed_on',)

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('staff', 'period', 'basic_salary', 'net_salary', 'status', 'disbursed_on')
    list_filter = ('status', 'period', 'created_at')
    search_fields = ('staff__first_name', 'staff__last_name', 'staff__email')
    readonly_fields = ('created_at', 'updated_at', 'gross_earnings', 'total_deductions', 'net_salary')
    fieldsets = (
        ('Basic Information', {'fields': ('period', 'staff', 'status')}),
        ('Salary Details', {
            'fields': ('basic_salary', 'gross_earnings', 'total_deductions', 'net_salary', 'days_worked', 'working_days')
        }),
        ('Approval', {'fields': ('approved_by', 'approval_date', 'disbursed_on')}),
        ('Other', {'fields': ('remarks',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'is_active')}),
    )

@admin.register(PayrollEarning)
class PayrollEarningAdmin(admin.ModelAdmin):
    list_display = ('payroll', 'description', 'amount', 'is_taxable')
    list_filter = ('is_taxable',)
    search_fields = ('payroll__staff__first_name', 'payroll__staff__last_name')

@admin.register(PayrollDeduction)
class PayrollDeductionAdmin(admin.ModelAdmin):
    list_display = ('payroll', 'description', 'amount')
    search_fields = ('payroll__staff__first_name', 'payroll__staff__last_name')
