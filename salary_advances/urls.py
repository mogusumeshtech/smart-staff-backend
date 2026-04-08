from django.urls import path, include
from rest_framework.routers import DefaultRouter
from salary_advances.views import SalaryAdvanceViewSet, SalaryAdvanceRecoveryViewSet

router = DefaultRouter()
router.register(r'advances', SalaryAdvanceViewSet, basename='salary-advance')
router.register(r'recoveries', SalaryAdvanceRecoveryViewSet, basename='salary-advance-recovery')

urlpatterns = [
    path('', include(router.urls)),
]
