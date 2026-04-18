from rest_framework import serializers
from salary_advances.models import SalaryAdvance, SalaryAdvanceRecovery

class SalaryAdvanceRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryAdvanceRecovery
        fields = ('id', 'payroll_month', 'amount_recovered', 'remarks')

class SalaryAdvanceSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.get_full_name', read_only=True)
    staff_id = serializers.CharField(source='staff.staff_id', read_only=True)
    request_date = serializers.SerializerMethodField()
    recoveries = SalaryAdvanceRecoverySerializer(many=True, read_only=True)

    class Meta:
        model = SalaryAdvance
        fields = (
            'id', 'staff', 'staff_name', 'staff_id', 'amount', 'reason', 'requested_date',
            'request_date', 'approval_date', 'disbursal_date', 'status', 'approved_by', 'remarks',
            'repayment_months', 'amount_recovered', 'recoveries', 'is_active', 'created_at'
        )
        read_only_fields = ('id', 'requested_date', 'created_at', 'amount_recovered')

    def get_request_date(self, obj):
        if obj.requested_date:
            return obj.requested_date.strftime('%Y-%m-%d')
        return None
