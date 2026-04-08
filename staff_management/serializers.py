from rest_framework import serializers
from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction

class StaffCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffCategory
        fields = ('id', 'name', 'description', 'is_active')

class DesignationSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Designation
        fields = ('id', 'name', 'category', 'category_name', 'salary_scale', 'description', 'is_active')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'head_name', 'description', 'is_active')

class StaffBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('id', 'staff_id', 'first_name', 'last_name', 'email', 'phone_number', 'designation', 'department')

class StaffSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Staff
        fields = (
            'id', 'staff_id', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'gender', 'marital_status', 'nationality', 'blood_group', 'mother_tongue',
            'category', 'category_name', 'designation', 'designation_name',
            'department', 'department_name', 'date_of_joining', 'status', 'basic_salary',
            'bank_account_number', 'bank_name', 'bank_branch', 'permanent_address', 'current_address',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'profile_picture', 'passport_photo', 'national_id', 'kra_pin',
            'passport_number', 'passport_expiry_date', 'qualification',
            'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class AllowanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance
        fields = ('id', 'name', 'description', 'amount', 'is_taxable', 'is_active')

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = ('id', 'name', 'description', 'percentage', 'is_active')
