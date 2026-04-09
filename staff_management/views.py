from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction
from staff_management.serializers import (
    StaffSerializer, StaffCategorySerializer, DesignationSerializer,
    DepartmentSerializer, AllowanceSerializer, DeductionSerializer, StaffBasicSerializer
)
import logging

logger = logging.getLogger(__name__)


class StaffCategoryViewSet(viewsets.ModelViewSet):
    queryset = StaffCategory.objects.all()  # Show ALL categories for management
    serializer_class = StaffCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()  # Show ALL designations
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()  # Show ALL departments
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
        # Use full serializer for both list and detail views
        return StaffSerializer

    def create(self, request, *args, **kwargs):
        """Override create to log and handle FormData properly"""
        try:
            # Log CRITICAL FIELDS that must be present
            critical_fields = ['category', 'gender', 'basic_salary', 'permanent_address', 'status', 'date_of_joining']
            available_fields = list(request.data.keys())

            logger.info("=" * 60)
            logger.info("NEW STAFF CREATION REQUEST")
            logger.info("=" * 60)

            logger.info(f"Total fields received: {len(available_fields)}")
            logger.info(f"Available fields: {available_fields}")

            # Check for critical fields
            for field in critical_fields:
                value = request.data.get(field)
                status_icon = "✓" if value else "✗"
                logger.info(f"{status_icon} {field}: {value}")

            logger.info(f"Raw request.data: {request.data}")

            serializer = self.get_serializer(data=request.data)
            is_valid = serializer.is_valid()

            if not is_valid:
                logger.error(f"Serializer validation errors: {serializer.errors}")
                raise Exception(f"Validation failed: {serializer.errors}")

            logger.info(f"Serializer is valid. Creating object...")
            self.perform_create(serializer)
            logger.info(f"✓ Staff created successfully with ID: {serializer.data.get('id')}")
            logger.info("=" * 60)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"✗ Error creating staff: {str(e)}")
            logger.error("=" * 60)
            raise

    def update(self, request, *args, **kwargs):
        """Override update to log and handle FormData properly"""
        try:
            critical_fields = ['category', 'gender', 'basic_salary', 'permanent_address', 'status', 'date_of_joining']
            available_fields = list(request.data.keys())
            staff_id = kwargs.get('pk')

            logger.info("=" * 60)
            logger.info(f"STAFF UPDATE REQUEST - ID: {staff_id}")
            logger.info("=" * 60)
            logger.info(f"Total fields received: {len(available_fields)}")
            logger.info(f"Available fields: {available_fields}")

            # Check for critical fields
            for field in critical_fields:
                value = request.data.get(field)
                status_icon = "✓" if value else "✗"
                logger.info(f"{status_icon} {field}: {value}")

            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)

            is_valid = serializer.is_valid()
            if not is_valid:
                logger.error(f"Serializer validation errors: {serializer.errors}")
                raise Exception(f"Validation failed: {serializer.errors}")

            self.perform_update(serializer)
            logger.info(f"✓ Staff updated successfully")
            logger.info("=" * 60)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"✗ Error updating staff: {str(e)}")
            logger.error("=" * 60)
            raise

class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = Allowance.objects.filter(is_active=True)
    serializer_class = AllowanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.filter(is_active=True)
    serializer_class = DeductionSerializer
    permission_classes = [permissions.IsAuthenticated]
