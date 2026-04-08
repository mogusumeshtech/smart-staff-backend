from django.urls import path, include
from rest_framework.routers import DefaultRouter
from staff_management.views import (
    StaffViewSet, StaffCategoryViewSet, DesignationViewSet,
    DepartmentViewSet, AllowanceViewSet, DeductionViewSet
)

router = DefaultRouter()
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'categories', StaffCategoryViewSet, basename='category')
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'allowances', AllowanceViewSet, basename='allowance')
router.register(r'deductions', DeductionViewSet, basename='deduction')

urlpatterns = [
    path('', include(router.urls)),
]
