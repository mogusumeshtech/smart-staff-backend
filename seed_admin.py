#!/usr/bin/env python
"""
Simple script to create admin user for SMART STAFF
Run this after migrations: python seed_admin.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    # Delete existing admin if it exists (fresh start)
    User.objects.filter(username='admin').delete()

    # Create fresh admin user
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@smartstaff.com',
        password='admin123'
    )

    print("✅ SUCCESS: Admin user created!")
    print(f"  Username: admin")
    print(f"  Password: admin123")
    print(f"  Email: admin@smartstaff.com")
    print(f"  User ID: {admin.id}")

    sys.exit(0)

except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

