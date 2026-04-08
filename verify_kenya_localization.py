#!/usr/bin/env python
"""
Kenya Localization Verification Script
Checks if SMART STAFF is properly localized for Kenya
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from staff_management.models import Staff
from django.db import connection

print("=" * 70)
print("SMART STAFF - KENYA LOCALIZATION VERIFICATION")
print("=" * 70)

# Check 1: Settings
print("\n✓ CHECK 1: Django Settings")
print(f"  Language Code: {settings.LANGUAGE_CODE}")
print(f"  Expected: en-ke | Actual: {settings.LANGUAGE_CODE}")
print(f"  ✅ PASS" if settings.LANGUAGE_CODE == 'en-ke' else "  ❌ FAIL")

print(f"\n  Time Zone: {settings.TIME_ZONE}")
print(f"  Expected: Africa/Nairobi | Actual: {settings.TIME_ZONE}")
print(f"  ✅ PASS" if settings.TIME_ZONE == 'Africa/Nairobi' else "  ❌ FAIL")

# Check 2: Database Schema - Staff Model Fields
print("\n✓ CHECK 2: Database Schema (Staff Model)")
staff_fields = [f.name for f in Staff._meta.get_fields()]

print("\n  Required Kenya Fields:")
kenya_fields = ['national_id', 'kra_pin', 'bank_branch']
for field in kenya_fields:
    status = "✅ Found" if field in staff_fields else "❌ Missing"
    print(f"    {field}: {status}")

print("\n  Removed India-Specific Fields (should NOT exist):")
india_fields = ['ifsc_code', 'aadhar_number', 'pan_number']
for field in india_fields:
    status = "✅ Not Found (Good!)" if field not in staff_fields else "❌ Still Exists"
    print(f"    {field}: {status}")

# Check 3: Database Actual Columns
print("\n✓ CHECK 3: Database Actual Columns")
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='staff_management_staff'
    """)
    db_columns = [row[0] for row in cursor.fetchall()]

print("\n  Checking Kenya fields in database:")
for field in kenya_fields:
    status = "✅ Found" if field in db_columns else "❌ Missing"
    print(f"    {field}: {status}")

print("\n  Checking removed India fields are gone:")
for field in india_fields:
    status = "✅ Not Found (Good!)" if field not in db_columns else "⚠️  Still exists"
    print(f"    {field}: {status}")

# Check 4: Sample Data
print("\n✓ CHECK 4: Sample Staff Records")
try:
    staff_count = Staff.objects.count()
    print(f"  Total Staff: {staff_count}")

    if staff_count > 0:
        sample_staff = Staff.objects.first()
        print(f"\n  Sample Staff Record:")
        print(f"    Name: {sample_staff.first_name} {sample_staff.last_name}")
        print(f"    Nationality: {sample_staff.nationality}")
        print(f"    National ID: {sample_staff.national_id or 'Not set'}")
        print(f"    KRA PIN: {sample_staff.kra_pin or 'Not set'}")
        print(f"    Bank Branch: {sample_staff.bank_branch or 'Not set'}")
        print(f"    Bank Name: {sample_staff.bank_name or 'Not set'}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Summary
print("\n" + "=" * 70)
print("LOCALIZATION STATUS SUMMARY")
print("=" * 70)

status_checks = {
    'Language Code (en-ke)': settings.LANGUAGE_CODE == 'en-ke',
    'Time Zone (Africa/Nairobi)': settings.TIME_ZONE == 'Africa/Nairobi',
    'National ID field exists': 'national_id' in staff_fields,
    'KRA PIN field exists': 'kra_pin' in staff_fields,
    'Bank Branch field exists': 'bank_branch' in staff_fields,
    'IFSC removed': 'ifsc_code' not in staff_fields,
    'Aadhar removed': 'aadhar_number' not in staff_fields,
    'PAN removed': 'pan_number' not in staff_fields,
}

passed = sum(1 for v in status_checks.values() if v)
total = len(status_checks)

print(f"\nPassed: {passed}/{total}")
for check, result in status_checks.items():
    status = "✅" if result else "❌"
    print(f"  {status} {check}")

print("\n" + "=" * 70)
if passed == total:
    print("✅ SMART STAFF IS FULLY LOCALIZED FOR KENYA!")
else:
    print(f"⚠️  LOCALIZATION INCOMPLETE - {total - passed} issues remaining")
print("=" * 70)
