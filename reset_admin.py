#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing admin if exists
User.objects.filter(username='admin').delete()

# Create new admin user
admin = User.objects.create_superuser(
    username='admin',
    email='admin@smartstaff.local',
    password='admin123'
)

print('✅ ADMIN CREDENTIALS RESET')
print('=' * 50)
print(f'Username: admin')
print(f'Password: admin123')
print(f'Status: ACTIVE')
print(f'Superuser: {admin.is_superuser}')
print('=' * 50)
