#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

# Now run the load command
from django.core.management import call_command

print("=" * 50)
print("SMART STAFF - Loading Sample Data")
print("=" * 50)
print()

try:
    call_command('load_sample_data')
    print()
    print("=" * 50)
    print("✅ Sample data loaded successfully!")
    print("=" * 50)

    # Verify counts
    from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction
    from salary_advances.models import SalaryAdvance
    from payroll.models import Payroll, PayrollPeriod
    from users.models import CustomUser

    print("\n📊 Data Verification:")
    print(f"  Users: {CustomUser.objects.count()}")
    print(f"  Staff: {Staff.objects.count()}")
    print(f"  Categories: {StaffCategory.objects.count()}")
    print(f"  Departments: {Department.objects.count()}")
    print(f"  Designations: {Designation.objects.count()}")
    print(f"  Payroll Records: {Payroll.objects.count()}")
    print(f"  Salary Advances: {SalaryAdvance.objects.count()}")
    print(f"  Allowances: {Allowance.objects.count()}")
    print(f"  Deductions: {Deduction.objects.count()}")
    print()
    print("🔐 You can now login with:")
    print("   admin / admin123")
    print("   hrmanager / hr123")
    print("   finance / finance123")
    print("   principal / principal123")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
