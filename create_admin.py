#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if admin already exists
if User.objects.filter(username='admin').exists():
    user = User.objects.get(username='admin')
    print(f"✓ Admin user '{user.username}' already exists")
    print(f"Email: {user.email}")
else:
    # Create superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@smartstaff.local',
        password='Admin@123'
    )
    print("✓ Superuser created successfully!")

print("\n" + "=" * 60)
print("📋 DJANGO ADMIN LOGIN CREDENTIALS")
print("=" * 60)
print(f"URL:      http://localhost:8000/admin")
print(f"Username: admin")
print(f"Password: Admin@123")
print("=" * 60)
