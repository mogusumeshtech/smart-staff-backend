from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SchoolSettings(BaseModel):
    """
    Centralized school settings model for branding and configuration.
    Singleton pattern - only one instance should exist.
    """
    school_name = models.CharField(max_length=255, default='Your School Name')
    school_address = models.TextField(blank=True)
    school_logo = models.ImageField(upload_to='school/', null=True, blank=True)
    app_name = models.CharField(max_length=255, default='SMART STAFF')
    timezone = models.CharField(max_length=50, default='Africa/Nairobi')
    date_format = models.CharField(max_length=20, default='DD/MM/YYYY')
    currency = models.CharField(max_length=10, default='KES')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # Notification Settings
    email_notifications = models.BooleanField(default=True)
    salary_advance_notifications = models.BooleanField(default=True)
    payroll_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    weekly_reports = models.BooleanField(default=True)
    monthly_reports = models.BooleanField(default=True)

    # Security Settings
    two_factor_auth = models.BooleanField(default=False)
    session_timeout = models.IntegerField(default=30)  # minutes
    auto_lock = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'School Settings'
        verbose_name_plural = 'School Settings'

    def __str__(self):
        return f'Settings for {self.school_name}'

    @staticmethod
    def get_settings():
        """Get or create the singleton settings instance"""
        settings, created = SchoolSettings.objects.get_or_create(pk=1)
        return settings
