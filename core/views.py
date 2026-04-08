from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect


def root_redirect(request):
    """
    Redirect root path to API v1 documentation.
    """
    return redirect('/api/v1/')


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    Root API endpoint that lists all available API resources.
    """
    base_url = request.build_absolute_uri('/api/v1')
    return Response({
        'message': 'Welcome to SMART STAFF API v1',
        'endpoints': {
            'auth': f'{base_url}/auth/',
            'staff': f'{base_url}/staff/',
            'salary_advances': f'{base_url}/salary-advances/',
            'payroll': f'{base_url}/payroll/',
            'reports': f'{base_url}/reports/',
        },
        'admin': f'{request.build_absolute_uri("/admin")}',
        'info': {
            'name': 'SMART STAFF - School Staff Management System',
            'version': '1.0.0',
            'description': 'A comprehensive system for managing school staff, payroll, salary advances, and reports.'
        }
    })
