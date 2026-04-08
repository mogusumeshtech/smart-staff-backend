from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.shortcuts import redirect
from .models import SchoolSettings
from .serializers import SchoolSettingsSerializer


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
            'settings': f'{base_url}/settings/',
        },
        'admin': f'{request.build_absolute_uri("/admin")}',
        'info': {
            'name': 'SMART STAFF - School Staff Management System',
            'version': '1.0.0',
            'description': 'A comprehensive system for managing school staff, payroll, salary advances, and reports.'
        }
    })


class SchoolSettingsViewSet(ModelViewSet):
    """
    ViewSet for managing school settings.
    Supports GET (retrieve), PUT/PATCH (update) operations.
    """
    queryset = SchoolSettings.objects.all()
    serializer_class = SchoolSettingsSerializer
    permission_classes = [AllowAny]  # Allow public access to settings

    def get_object(self):
        """Always return the singleton settings instance"""
        obj, created = SchoolSettings.objects.get_or_create(pk=1)
        return obj

    def list(self, request, *args, **kwargs):
        """Return the singleton settings instance"""
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Update the singleton settings instance (instead of creating)"""
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
