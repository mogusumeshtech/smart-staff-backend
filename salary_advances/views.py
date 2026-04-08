from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from salary_advances.models import SalaryAdvance, SalaryAdvanceRecovery
from salary_advances.serializers import SalaryAdvanceSerializer, SalaryAdvanceRecoverySerializer

class SalaryAdvanceViewSet(viewsets.ModelViewSet):
    queryset = SalaryAdvance.objects.all()
    serializer_class = SalaryAdvanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'staff']
    search_fields = ['staff__first_name', 'staff__last_name', 'staff__email']
    ordering_fields = ['requested_date', 'amount']
    ordering = ['-requested_date']

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        """Approve a salary advance request"""
        try:
            salary_advance = self.get_object()
            salary_advance.status = 'approved'
            salary_advance.save()
            serializer = self.get_serializer(salary_advance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """Reject a salary advance request"""
        try:
            salary_advance = self.get_object()
            salary_advance.status = 'rejected'
            salary_advance.save()
            serializer = self.get_serializer(salary_advance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def disburse(self, request, pk=None):
        """Disburse an approved salary advance"""
        try:
            salary_advance = self.get_object()
            salary_advance.status = 'disbursed'
            salary_advance.save()
            serializer = self.get_serializer(salary_advance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SalaryAdvanceRecoveryViewSet(viewsets.ModelViewSet):
    queryset = SalaryAdvanceRecovery.objects.all()
    serializer_class = SalaryAdvanceRecoverySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['salary_advance', 'payroll_month']
