from rest_framework import serializers
from payroll.models import PayrollPeriod, Payroll, PayrollEarning, PayrollDeduction
from staff_management.serializers import StaffSerializer

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
    staff_details = serializers.SerializerMethodField()

    class Meta:
        model = Payroll
        fields = (
            'id', 'period', 'period_display', 'staff', 'staff_name', 'staff_details',
            'basic_salary', 'gross_earnings', 'total_deductions', 'net_salary',
            'days_worked', 'working_days', 'status', 'approved_by', 'approval_date',
            'disbursed_on', 'remarks', 'earnings', 'deductions', 'created_at'
        )
        read_only_fields = ('id', 'gross_earnings', 'total_deductions', 'net_salary', 'created_at')

    def get_staff_details(self, obj):
        """Return full staff details for receipt display."""
        return {
            'first_name': obj.staff.first_name,
            'last_name': obj.staff.last_name,
            'staff_id': obj.staff.staff_id,
            'designation_name': obj.staff.designation.name if obj.staff.designation else 'N/A',
            'department_name': obj.staff.department.name if obj.staff.department else 'N/A'
        }

    def create(self, validated_data):
        """Create payroll and ensure salary calculations are done."""
        payroll = Payroll(**validated_data)
        payroll.calculate_earnings_deductions()  # Manually trigger calculation
        payroll.save()
        return payroll

    def update(self, instance, validated_data):
        """Update payroll and recalculate salary values."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.calculate_earnings_deductions()  # Recalculate on update
        instance.save()
        return instance

class PayrollSummarySerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.get_full_name', read_only=True)
    period_display = serializers.CharField(source='period.__str__', read_only=True)
    staff_details = serializers.SerializerMethodField()
    deductions = PayrollDeductionSerializer(many=True, read_only=True)

    class Meta:
        model = Payroll
        fields = ('id', 'staff', 'staff_name', 'staff_details', 'period_display',
                  'basic_salary', 'gross_earnings', 'total_deductions', 'net_salary',
                  'status', 'disbursed_on', 'deductions')

    def get_staff_details(self, obj):
        """Return full staff details for receipt display."""
        return {
            'first_name': obj.staff.first_name,
            'last_name': obj.staff.last_name,
            'staff_id': obj.staff.staff_id,
            'designation_name': obj.staff.designation.name if obj.staff.designation else 'N/A',
            'department_name': obj.staff.department.name if obj.staff.department else 'N/A'
        }
