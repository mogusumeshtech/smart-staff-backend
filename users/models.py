from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('hr_manager', 'HR Manager'),
        ('finance', 'Finance Manager'),
        ('principal', 'Principal'),
        ('staff_member', 'Staff Member'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff_member')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
