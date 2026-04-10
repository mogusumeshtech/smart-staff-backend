#!/usr/bin/env python
"""
Startup script for SMART STAFF on Render
Handles migrations safely without blocking if database isn't ready
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Initialize Django
    django.setup()

    # Try to run migrations - but don't fail if DB isn't ready
    print("🔧 Attempting migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed")
    except Exception as e:
        print(f"⚠️  Migrations skipped: {str(e)[:100]}")

    # Try to collect static files
    print("📦 Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected")
    except Exception as e:
        print(f"⚠️  Static files skipped: {str(e)[:100]}")
