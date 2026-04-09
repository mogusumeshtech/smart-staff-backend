#!/usr/bin/env python3
"""
DIAGNOSTIC SCRIPT - Test backend configuration and data integrity
Run: python diagnose.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from staff_management.models import Staff, StaffCategory, Designation, Department
from core.models import SchoolSettings
from rest_framework.test import APIRequestFactory
from staff_management.serializers import StaffSerializer

print("=" * 80)
print("🔍 SMART STAFF SYSTEM DIAGNOSTIC")
print("=" * 80)

# Test 1: Database connection
print("\n1️⃣  DATABASE CONNECTION")
print("-" * 80)
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database connection: OK")
except Exception as e:
    print(f"❌ Database connection FAILED: {e}")
    sys.exit(1)

# Test 2: Check data in database
print("\n2️⃣  DATA IN DATABASE")
print("-" * 80)
staff_count = Staff.objects.count()
print(f"Total staff members: {staff_count}")

if staff_count > 0:
    first_staff = Staff.objects.first()
    print(f"\n📋 First staff record:")
    print(f"  ID: {first_staff.id}")
    print(f"  Name: {first_staff.first_name} {first_staff.last_name}")
    print(f"  Email: {first_staff.email}")
    print(f"  Basic Salary: {first_staff.basic_salary}")
    print(f"  Status: {first_staff.status}")
    print(f"  Is Active: {first_staff.is_active}")
    print(f"  Category: {first_staff.category.name if first_staff.category else 'NONE'}")
    print(f"  Designation: {first_staff.designation.name if first_staff.designation else 'NONE'}")
    print(f"  Department: {first_staff.department.name if first_staff.department else 'NONE'}")
else:
    print("⚠️  No staff members in database")

# Test 3: Check serializer output
print("\n3️⃣  SERIALIZER OUTPUT TEST")
print("-" * 80)
if staff_count > 0:
    serializer = StaffSerializer(first_staff)
    data = serializer.data
    print(f"Serialized fields: {list(data.keys())}")
    print(f"\nCritical fields in output:")
    print(f"  designation_name: {data.get('designation_name', 'MISSING')}")
    print(f"  department_name: {data.get('department_name', 'MISSING')}")
    print(f"  category_name: {data.get('category_name', 'MISSING')}")
    print(f"  basic_salary: {data.get('basic_salary', 'MISSING')}")
    print(f"  status: {data.get('status', 'MISSING')}")
    print(f"  is_active: {data.get('is_active', 'MISSING')}")

# Test 4: Check categories
print("\n4️⃣  CATEGORIES")
print("-" * 80)
categories = StaffCategory.objects.all()
print(f"Total categories: {categories.count()}")
for cat in categories[:5]:
    print(f"  ✓ {cat.name} (is_active={cat.is_active})")

# Test 5: Check settings
print("\n5️⃣  SCHOOL SETTINGS")
print("-" * 80)
try:
    settings = SchoolSettings.objects.first()
    if settings:
        print(f"✅ Settings found:")
        print(f"  School name: {settings.school_name}")
        print(f"  School address: {settings.school_address}")
        print(f"  Logo: {settings.school_logo if settings.school_logo else 'NONE'}")
    else:
        print("⚠️  No settings found in database")
except Exception as e:
    print(f"❌ Settings check failed: {e}")

# Test 6: Check for inactive staff
print("\n6️⃣  STAFF STATUS CHECK")
print("-" * 80)
active_staff = Staff.objects.filter(is_active=True).count()
inactive_staff = Staff.objects.filter(is_active=False).count()
print(f"Active staff: {active_staff}")
print(f"Inactive staff: {inactive_staff}")

if inactive_staff > 0:
    print("\n⚠️  INACTIVE STAFF FOUND:")
    for staff in Staff.objects.filter(is_active=False)[:5]:
        print(f"  - {staff.first_name} {staff.last_name} (ID: {staff.id})")

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC COMPLETE")
print("=" * 80)
