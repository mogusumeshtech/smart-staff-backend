#!/usr/bin/env python
"""
Quick test to verify payroll calculation is working correctly.
Run with: python test_payroll_calculation.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decimal import Decimal
from payroll.models import Payroll, PayrollPeriod
from staff_management.models import Staff

# Get or create a test period
period, _ = PayrollPeriod.objects.get_or_create(
    month=4,
    year=2026,
    defaults={'start_date': '2026-04-01', 'end_date': '2026-04-30', 'status': 'draft'}
)

# Get a staff member
staff = Staff.objects.first()

if not staff:
    print("ERROR: No staff members found in database")
    exit(1)

# Create a test payroll
payroll = Payroll(
    period=period,
    staff=staff,
    basic_salary=Decimal('50000.00'),
)

print(f"Created payroll for {staff.get_full_name()}")
print(f"Basic salary: {payroll.basic_salary}")
print(f"Before save - Gross earnings: {payroll.gross_earnings}")
print(f"Before save - Total deductions: {payroll.total_deductions}")
print(f"Before save - Net salary: {payroll.net_salary}")

# Save should trigger calculation
payroll.save()

print(f"\nAfter save:")
print(f"Gross earnings: {payroll.gross_earnings}")
print(f"Total deductions: {payroll.total_deductions}")
print(f"Net salary: {payroll.net_salary}")

# Verify calculations
expected_gross = Decimal('50000.00') * Decimal('1.2')  # 60000
expected_deductions = Decimal('50000.00') * Decimal('0.15')  # 7500
expected_net = expected_gross - expected_deductions  # 52500

print(f"\nExpected gross earnings: {expected_gross}")
print(f"Expected total deductions: {expected_deductions}")
print(f"Expected net salary: {expected_net}")

if payroll.gross_earnings == expected_gross and payroll.total_deductions == expected_deductions and payroll.net_salary == expected_net:
    print("\n✅ PAYROLL CALCULATION TEST PASSED!")
else:
    print("\n❌ PAYROLL CALCULATION TEST FAILED!")
    print(f"Gross mismatch: {payroll.gross_earnings} != {expected_gross}")
    print(f"Deductions mismatch: {payroll.total_deductions} != {expected_deductions}")
    print(f"Net mismatch: {payroll.net_salary} != {expected_net}")
