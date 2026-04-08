from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction
from staff_management.serializers import (
    StaffSerializer, StaffCategorySerializer, DesignationSerializer,
    DepartmentSerializer, AllowanceSerializer, DeductionSerializer, StaffBasicSerializer
)

class StaffCategoryViewSet(viewsets.ModelViewSet):
    queryset = StaffCategory.objects.filter(is_active=True)
    serializer_class = StaffCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.filter(is_active=True)
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'designation', 'department', 'status', 'gender']
    search_fields = ['staff_id', 'first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = ['first_name', 'created_at', 'basic_salary']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return StaffBasicSerializer
        return StaffSerializer

class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = Allowance.objects.filter(is_active=True)
    serializer_class = AllowanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.filter(is_active=True)
    serializer_class = DeductionSerializer
    permission_classes = [permissions.IsAuthenticated]
