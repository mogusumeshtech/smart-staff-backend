#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Create admin user if it doesn't exist
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@smartstaff.com',
        password='admin123'
    )
    print(f"✅ Admin user created: {admin.username}")
else:
    # Update password if user exists
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.save()
    print(f"✅ Admin user password updated")

print("Login credentials:")
print("  Username: admin")
print("  Password: admin123")
