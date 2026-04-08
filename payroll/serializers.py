from rest_framework import serializers
from payroll.models import PayrollPeriod, Payroll, PayrollEarning, PayrollDeduction

class PayrollPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPeriod
        fields = ('id', 'month', 'year', 'start_date', 'end_date', 'status', 'processed_by', 'processed_on')
        read_only_fields = ('processed_on',)

class PayrollEarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollEarning
        fields = ('id', 'description', 'amount', 'is_taxable')

class PayrollDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollDeduction
        fields = ('id', 'description', 'amount')

class PayrollSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.get_full_name', read_only=True)
    period_display = serializers.CharField(source='period.__str__', read_only=True)
    earnings = PayrollEarningSerializer(many=True, read_only=True)
    deductions = PayrollDeductionSerializer(many=True, read_only=True)

    class Meta:
        model = Payroll
        fields = (
            'id', 'period', 'period_display', 'staff', 'staff_name', 'basic_salary',
            'gross_earnings', 'total_deductions', 'net_salary', 'days_worked', 'working_days',
            'status', 'approved_by', 'approval_date', 'disbursed_on', 'remarks',
            'earnings', 'deductions', 'is_active', 'created_at'
        )
        read_only_fields = ('id', 'gross_earnings', 'total_deductions', 'net_salary', 'created_at')

class PayrollSummarySerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.get_full_name', read_only=True)

    class Meta:
        model = Payroll
        fields = ('id', 'staff', 'staff_name', 'net_salary', 'status', 'disbursed_on')
