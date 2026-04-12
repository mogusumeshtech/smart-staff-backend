#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Check if admin exists
if User.objects.filter(username='admin').exists():
    print("✅ Admin user already exists")
    admin = User.objects.get(username='admin')
    print(f"   Username: {admin.username}")
    print(f"   Email: {admin.email}")
else:
    user = User.objects.create_superuser(
        username='admin',
        email='admin@smartstaff.local',
        password='admin123456',
        first_name='Admin',
        last_name='User'
    )
    print(f"✅ Created admin user!")
    print(f"   Username: {user.username}")
    print(f"   Password: admin123456")
    print(f"   Email: {user.email}")

# Show all users
print("\n📋 All users in database:")
for u in User.objects.all():
    print(f"   - {u.username:20} | staff: {str(u.is_staff):5} | superuser: {u.is_superuser}")
