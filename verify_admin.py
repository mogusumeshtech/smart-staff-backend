#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

print("=" * 60)
print("ADMIN ACCOUNT VERIFICATION")
print("=" * 60)

# Check admin user
admin = User.objects.filter(username='admin').first()
if admin:
    print(f"✓ Admin user found")
    print(f"  Username: {admin.username}")
    print(f"  Is superuser: {admin.is_superuser}")
    print(f"  Is staff: {admin.is_staff}")
    print(f"  Email: {admin.email}")
    print()

    # Try to authenticate
    user = authenticate(username='admin', password='Admin@123')
    if user:
        print(f"✓ Authentication SUCCESSFUL with current password")
    else:
        print(f"✗ Authentication FAILED - password may be incorrect")
        print("  Resetting password to 'Admin@123'...")
        admin.set_password('Admin@123')
        admin.save()
        print("  ✓ Password reset complete")
else:
    print("✗ Admin user not found - creating new one...")
    User.objects.create_superuser('admin', 'admin@smartstaff.local', 'Admin@123')
    print("✓ Admin user created successfully")

print()
print("=" * 60)
print("ACCESS CREDENTIALS")
print("=" * 60)
print(f"URL:      http://localhost:8000/admin")
print(f"Username: admin")
print(f"Password: Admin@123")
print("=" * 60)
