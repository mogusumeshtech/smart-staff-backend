from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView  # Temporarily disabled
from django.conf import settings
from django.conf.urls.static import static
from core.views import root_redirect, api_root, SchoolSettingsViewSet
from staff_management.views import (
    StaffViewSet, StaffCategoryViewSet, DesignationViewSet,
    DepartmentViewSet, AllowanceViewSet, DeductionViewSet
)
from users.views import UserViewSet, login
from payroll.views import PayrollViewSet, PayrollPeriodViewSet
from salary_advances.views import SalaryAdvanceViewSet
from reports.views import ReportViewSet

# Create a single router for all viewsets
router = DefaultRouter()
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'categories', StaffCategoryViewSet, basename='category')
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'allowances', AllowanceViewSet, basename='allowance')
router.register(r'deductions', DeductionViewSet, basename='deduction')
router.register(r'users', UserViewSet, basename='user')
router.register(r'payroll-periods', PayrollPeriodViewSet, basename='payroll-period')
router.register(r'payroll', PayrollViewSet, basename='payroll')
router.register(r'salary-advances', SalaryAdvanceViewSet, basename='salary-advance')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'settings', SchoolSettingsViewSet, basename='settings')

urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Temporarily disabled
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Temporarily disabled
    path('api/v1/', api_root, name='api-root'),
    path('api/v1/auth/login/', login, name='login'),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# admin.site.site_header = 'SMART STAFF Administration'  # DISABLED
