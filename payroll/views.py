from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from payroll.models import PayrollPeriod, Payroll, PayrollEarning, PayrollDeduction
from payroll.serializers import (
    PayrollPeriodSerializer, PayrollSerializer, PayrollEarningSerializer,
    PayrollDeductionSerializer, PayrollSummarySerializer
)

class PayrollPeriodViewSet(viewsets.ModelViewSet):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'year', 'month']
    ordering_fields = ['year', 'month']
    ordering = ['-year', '-month']

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['period', 'staff', 'status']
    search_fields = ['staff__first_name', 'staff__last_name', 'staff__email']
    ordering_fields = ['period', 'net_salary', 'status']
    ordering = ['-period']

    def get_serializer_class(self):
        if self.action == 'list':
            return PayrollSummarySerializer
        return PayrollSerializer

class PayrollEarningViewSet(viewsets.ModelViewSet):
    queryset = PayrollEarning.objects.all()
    serializer_class = PayrollEarningSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payroll']

class PayrollDeductionViewSet(viewsets.ModelViewSet):
    queryset = PayrollDeduction.objects.all()
    serializer_class = PayrollDeductionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payroll']
