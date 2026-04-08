from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payroll.views import (
    PayrollPeriodViewSet, PayrollViewSet, PayrollEarningViewSet,
    PayrollDeductionViewSet
)

router = DefaultRouter()
router.register(r'periods', PayrollPeriodViewSet, basename='payroll-period')
router.register(r'payrolls', PayrollViewSet, basename='payroll')
router.register(r'earnings', PayrollEarningViewSet, basename='payroll-earning')
router.register(r'deductions', PayrollDeductionViewSet, basename='payroll-deduction')

urlpatterns = [
    path('', include(router.urls)),
]
