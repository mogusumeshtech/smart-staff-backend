#!/usr/bin/env python
"""Fix admin user login"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import CustomUser

print("=" * 60)
print("🔐 FIXING ADMIN LOGIN")
print("=" * 60)

# Check if admin exists
admin_exists = CustomUser.objects.filter(username='admin').exists()
print(f"\nAdmin user exists: {admin_exists}")

if admin_exists:
    user = CustomUser.objects.get(username='admin')
    user.set_password('admin123')
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"\n✓ Password updated to: admin123")
else:
    print("\nCreating admin user...")
    user = CustomUser.objects.create_user(
        username='admin',
        email='admin@smartstaff.local',
        password='admin123',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    print(f"✓ Admin user created")

print(f"✓ Username: admin")
print(f"✓ Password: admin123")
print(f"✓ Email: {user.email}")
print(f"✓ Is active: {user.is_active}")
print(f"✓ Is superuser: {user.is_superuser}")
print("\n" + "=" * 60)
print("✅ LOGIN CREDENTIALS READY")
print("=" * 60)
print("\nTry logging in again with:")
print("  Username: admin")
print("  Password: admin123")
