from rest_framework import serializers
from salary_advances.models import SalaryAdvance, SalaryAdvanceRecovery

class SalaryAdvanceRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryAdvanceRecovery
        fields = ('id', 'payroll_month', 'amount_recovered', 'remarks')

class SalaryAdvanceSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.get_full_name', read_only=True)
    recoveries = SalaryAdvanceRecoverySerializer(many=True, read_only=True)

    class Meta:
        model = SalaryAdvance
        fields = (
            'id', 'staff', 'staff_name', 'amount', 'reason', 'requested_date',
            'approval_date', 'disbursal_date', 'status', 'approved_by', 'remarks',
            'repayment_months', 'amount_recovered', 'recoveries', 'is_active', 'created_at'
        )
        read_only_fields = ('id', 'requested_date', 'created_at', 'amount_recovered')
