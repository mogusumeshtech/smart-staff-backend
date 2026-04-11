from django.contrib import admin
from .models import SchoolSettings


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'app_name', 'timezone', 'currency', 'updated_at')
    fieldsets = (
        ('School Information', {
            'fields': ('school_name', 'school_address', 'school_logo', 'phone', 'email', 'website')
        }),
        ('Application Settings', {
            'fields': ('app_name', 'timezone', 'date_format', 'currency')
        }),
        ('Notification Settings', {
            'fields': (
                'email_notifications',
                'salary_advance_notifications',
                'payroll_notifications',
                'system_notifications',
                'weekly_reports',
                'monthly_reports',
            )
        }),
        ('Security Settings', {
            'fields': ('two_factor_auth', 'session_timeout', 'auto_lock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        """Allow only one settings instance to exist in the database"""
        return False if SchoolSettings.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of settings"""
        return False
