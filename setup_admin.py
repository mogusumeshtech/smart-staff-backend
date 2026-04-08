#!/usr/bin/env python
"""Set admin user password"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import CustomUser

try:
    user = CustomUser.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print(f'✓ Admin password set to: admin123')
    print(f'✓ Admin email: {user.email}')
    print(f'✓ Total users: {CustomUser.objects.count()}')
    print(f'✓ Ready to login!')
except Exception as e:
    print(f'Error: {e}')
