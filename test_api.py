#!/usr/bin/env python
"""Test API endpoints locally"""

import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from staff_management.models import Staff, Department, Designation
from payroll.models import PayrollPeriod, Payroll
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()

# Create a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@test.com',
        'is_staff': False,
        'is_superuser': False
    }
)
if created:
    user.set_password('test123')
    user.save()
    print(f"✓ Created user: {user.username}")
else:
    print(f"✓ User exists: {user.username}")

# Get token
refresh = RefreshToken.for_user(user)
token = str(refresh.access_token)
print(f"\n✓ JWT Token: {token[:50]}...")

# Create test staff if needed
dept, _ = Department.objects.get_or_create(name='Test Dept')
desig, _ = Designation.objects.get_or_create(
    name='Tester',
    defaults={'salary_scale': Decimal('1000.00')}
)

staff, created = Staff.objects.get_or_create(
    email='staff@test.com',
    defaults={
        'first_name': 'Test',
        'last_name': 'Staff',
        'staff_id': 'TST001',
        'department': dept,
        'designation': desig,
        'basic_salary': Decimal('50000.00'),
        'employment_type': 'permanent',
        'status': 'active'
    }
)
if created:
    print(f"✓ Created staff: {staff.get_full_name()}")
else:
    print(f"✓ Staff exists: {staff.get_full_name()}")

# Create payroll period if needed
period, created = PayrollPeriod.objects.get_or_create(
    month=4,
    year=2024,
    defaults={
        'start_date': '2024-04-01',
        'end_date': '2024-04-30',
        'status': 'draft'
    }
)
if created:
    print(f"✓ Created period: {period}")
else:
    print(f"✓ Period exists: {period}")

# Test payroll creation
print(f"\nTesting payroll creation...")
try:
    payroll = Payroll.objects.create(
        period=period,
        staff=staff,
        basic_salary=Decimal('50000.00'),
        status='draft'
    )
    print(f"✓ Created payroll: {payroll}")
    print(f"  - Gross Earnings: {payroll.gross_earnings}")
    print(f"  - Total Deductions: {payroll.total_deductions}")
    print(f"  - Net Salary: {payroll.net_salary}")
    print(f"  - Deductions count: {payroll.deductions.count()}")

    for d in payroll.deductions.all():
        print(f"    - {d.description}: {d.amount}")

except Exception as e:
    print(f"✗ Error creating payroll: {e}")
    import traceback
    traceback.print_exc()

print("\n✓ API tests completed")
