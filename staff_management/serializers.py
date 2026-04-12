from rest_framework import serializers
from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction, StaffDeductionConfig

class StaffCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffCategory
        fields = ('id', 'name', 'description', 'is_active')

    def create(self, validated_data):
        """Ensure new categories are created as active"""
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
        return super().create(validated_data)

class DesignationSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Designation
        fields = ('id', 'name', 'category', 'category_name', 'salary_scale', 'description', 'is_active')

    def create(self, validated_data):
        """Ensure new designations are created as active"""
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
        return super().create(validated_data)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'head_name', 'description', 'is_active')

    def create(self, validated_data):
        """Ensure new departments are created as active"""
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
        return super().create(validated_data)

class StaffBasicSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Staff
        fields = '__all__'  # Return ALL fields in list view too
        read_only_fields = ('id', 'created_at', 'updated_at', 'category_name', 'designation_name', 'department_name')

class StaffSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Staff
        # CRITICAL: Explicitly list ALL fields including computed ones
        fields = ('id', 'staff_id', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number',
                  'date_of_birth', 'gender', 'category', 'category_name',
                  'designation', 'designation_name', 'department', 'department_name',
                  'date_of_joining', 'status', 'basic_salary',
                  'bank_account_number', 'bank_name', 'bank_branch',
                  'permanent_address', 'current_address',
                  'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
                  'profile_picture', 'passport_photo', 'national_id', 'kra_pin',
                  'passport_number', 'passport_expiry_date', 'marital_status',
                  'nationality', 'qualification', 'mother_tongue', 'blood_group',
                  'created_at', 'updated_at', 'is_active')
        read_only_fields = ('id', 'created_at', 'updated_at', 'category_name', 'designation_name', 'department_name')

    def create(self, validated_data):
        """Ensure new staff are created as active"""
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
        return super().create(validated_data)

class AllowanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance
        fields = ('id', 'name', 'description', 'amount', 'is_taxable', 'is_active')

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = ('id', 'name', 'description', 'percentage', 'amount', 'is_active')


class StaffDeductionConfigSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.get_full_name', read_only=True)

    class Meta:
        model = StaffDeductionConfig
        fields = (
            'id', 'staff', 'staff_name', 'apply_paye', 'apply_nssf',
            'apply_sha', 'sha_amount', 'apply_housing_levy',
            'full_salary', 'notes'
        )
