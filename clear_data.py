#!/usr/bin/env python
"""
Clear all sample data from the database
Run: python manage.py shell < clear_data.py
Or: python clear_data.py
"""

import os
import django

# Setup Django if running standalone
try:
    django.setup()
except:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from django.contrib.auth.models import User
from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction
from payroll.models import Payroll, PayrollPeriod, PayrollEarning, PayrollDeduction
from salary_advances.models import SalaryAdvance
from users.models import CustomUser

print("=" * 60)
print("🗑️  CLEARING ALL SAMPLE DATA")
print("=" * 60)

# Count before
print("\nBefore clearing:")
print(f"  Users: {User.objects.count()}")
print(f"  Custom Users: {CustomUser.objects.count()}")
print(f"  Staff Members: {Staff.objects.count()}")
print(f"  Payroll Records: {Payroll.objects.count()}")
print(f"  Payroll Periods: {PayrollPeriod.objects.count()}")
print(f"  Salary Advances: {SalaryAdvance.objects.count()}")
print(f"  Designations: {Designation.objects.count()}")
print(f"  Departments: {Department.objects.count()}")
print(f"  Staff Categories: {StaffCategory.objects.count()}")

# Delete data in correct order (respect foreign keys)
print("\nDeleting data...")
PayrollDeduction.objects.all().delete()
PayrollEarning.objects.all().delete()
Payroll.objects.all().delete()
PayrollPeriod.objects.all().delete()
SalaryAdvance.objects.all().delete()
Deduction.objects.all().delete()
Allowance.objects.all().delete()
Staff.objects.all().delete()
Designation.objects.all().delete()
Department.objects.all().delete()
StaffCategory.objects.all().delete()
CustomUser.objects.all().delete()
User.objects.all().delete()

print("✓ Data deleted")

# Verify
print("\nAfter clearing:")
print(f"  Users: {User.objects.count()}")
print(f"  Custom Users: {CustomUser.objects.count()}")
print(f"  Staff Members: {Staff.objects.count()}")
print(f"  Payroll Records: {Payroll.objects.count()}")
print(f"  Payroll Periods: {PayrollPeriod.objects.count()}")
print(f"  Salary Advances: {SalaryAdvance.objects.count()}")

print("\n" + "=" * 60)
print("✅ DATABASE CLEARED - System is ready for fresh setup")
print("=" * 60)
