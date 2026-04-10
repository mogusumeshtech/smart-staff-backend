#!/usr/bin/env python
"""
Initialization script that loads sample data on first Render deployment
Run with: python initialize_production.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from staff_management.models import Staff

User = get_user_model()

# Create superuser if doesn't exist
admin_exists = User.objects.filter(username='admin').exists()
if not admin_exists:
    print("👤 Creating admin superuser...")
    try:
        User.objects.create_superuser('admin', 'admin@school.com', 'admin123')
        print("✅ Admin superuser created successfully!")
    except Exception as e:
        print(f"⚠️  Error creating admin superuser: {e}")

# Collect static files
print("📦 Collecting static files...")
try:
    call_command('collectstatic', '--noinput', verbosity=0)
    print("✅ Static files collected!")
except Exception as e:
    print(f"⚠️  Error collecting static files: {e}")

# Check if database is empty and load sample data
staff_count = Staff.objects.count()

if staff_count == 0:
    print("📦 Database is empty. Loading sample data...")
    try:
        call_command('load_sample_data', verbosity=2)
        print("✅ Sample data loaded successfully!")
    except Exception as e:
        print(f"⚠️ Error loading sample data: {e}")
        sys.exit(1)
else:
    print(f"✅ Database has {staff_count} staff members. Skipping data load.")

print("✅ Production initialization complete!")
