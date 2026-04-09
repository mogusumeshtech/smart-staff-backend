from rest_framework import serializers
from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction

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
        fields = '__all__'  # Accept and save ALL fields from the model
        read_only_fields = ('id', 'created_at', 'updated_at', 'category_name', 'designation_name', 'department_name')

class AllowanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance
        fields = ('id', 'name', 'description', 'amount', 'is_taxable', 'is_active')

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = ('id', 'name', 'description', 'percentage', 'is_active')
