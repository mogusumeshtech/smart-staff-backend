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
from staff_management.models import Staff

# Check if database is empty
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
