from rest_framework import serializers
from .models import SchoolSettings


class SchoolSettingsSerializer(serializers.ModelSerializer):
    school_logo_url = serializers.SerializerMethodField()

    class Meta:
        model = SchoolSettings
        fields = [
            'id',
            'school_name',
            'school_address',
            'school_logo',
            'school_logo_url',
            'app_name',
            'timezone',
            'date_format',
            'currency',
            'phone',
            'email',
            'website',
            'email_notifications',
            'salary_advance_notifications',
            'payroll_notifications',
            'system_notifications',
            'weekly_reports',
            'monthly_reports',
            'two_factor_auth',
            'session_timeout',
            'auto_lock',
            'created_at',
            'updated_at',
        ]

    def get_school_logo_url(self, obj):
        """Get the full URL of the school logo"""
        if obj.school_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.school_logo.url)
            return obj.school_logo.url
        return None
