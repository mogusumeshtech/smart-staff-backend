"""
Diagnostic endpoint to check Django settings and environment
Add to urls.py to enable: path('api/v1/diagnostics/', diagnostics_view),
"""

from django.http import JsonResponse
from django.conf import settings
import os
import sys

def diagnostics_view(request):
    """Return diagnostic information about the Django setup."""
    return JsonResponse({
        "status": "ok",
        "debug": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "database_engine": settings.DATABASES['default']['ENGINE'],
        "installed_apps": settings.INSTALLED_APPS,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "environment": {
            "DEBUG": os.getenv('DEBUG', 'NOT SET'),
            "SECRET_KEY": "***HIDDEN***" if os.getenv('SECRET_KEY') else "NOT SET",
            "DATABASE_URL": "***HIDDEN***" if os.getenv('DATABASE_URL') else "NOT SET",
            "ALLOWED_HOSTS": os.getenv('ALLOWED_HOSTS', 'NOT SET'),
            "CORS_ALLOWED_ORIGINS": os.getenv('CORS_ALLOWED_ORIGINS', 'NOT SET'),
        },
        "static_files": {
            "STATIC_URL": settings.STATIC_URL,
            "STATIC_ROOT": str(settings.STATIC_ROOT),
        },
        "auth_user_model": settings.AUTH_USER_MODEL,
        "custom_user_model_active": True,
    }, safe=False)
