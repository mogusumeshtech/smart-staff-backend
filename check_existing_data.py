#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from staff_management.models import Staff, Category, Designation, Department
from payroll.models import PayrollPeriod, Payroll, Earnings, Deductions
from salary_advances.models import SalaryAdvance
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*80)
print("SMART STAFF DATABASE AUDIT - APRIL 13, 2026")
print("="*80)

# Users
print("\n[USERS]")
users = User.objects.all()
print(f"Total Users: {users.count()}")
for user in users:
    print(f"  - {user.username} ({user.email}) - Staff: {user.is_staff}")

# Categories
print("\n[CATEGORIES]")
categories = Category.objects.all()
print(f"Total Categories: {categories.count()}")
for cat in categories:
    print(f"  - {cat.name}")

# Designations
print("\n[DESIGNATIONS]")
designations = Designation.objects.all()
print(f"Total Designations: {designations.count()}")
for des in designations:
    print(f"  - {des.name} (Base Salary: {des.base_salary})")

# Departments
print("\n[DEPARTMENTS]")
departments = Department.objects.all()
print(f"Total Departments: {departments.count()}")
for dept in departments:
    print(f"  - {dept.name} (Head: {dept.department_head})")

# Staff
print("\n[STAFF MEMBERS]")
staff = Staff.objects.all()
print(f"Total Staff: {staff.count()}")
for s in staff:
    print(f"  - {s.staff_id}: {s.first_name} {s.last_name}")
    print(f"    Department: {s.department}")
    print(f"    Designation: {s.designation}")
    print(f"    Status: {s.employment_status}")
    print(f"    Email: {s.email}")
    print(f"    Phone: {s.phone_number}")

# Payroll Periods
print("\n[PAYROLL PERIODS]")
periods = PayrollPeriod.objects.all()
print(f"Total Payroll Periods: {periods.count()}")
for period in periods:
    print(f"  - {period.month}/{period.year} (Status: {period.status})")

# Payroll Records
print("\n[PAYROLL RECORDS]")
payrolls = Payroll.objects.all()
print(f"Total Payroll Records: {payrolls.count()}")
for p in payrolls:
    print(f"  - {p.staff}: {p.payroll_period} (Status: {p.status}, Gross: {p.gross_salary})")

# Earnings
print("\n[EARNINGS]")
earnings = Earnings.objects.all()
print(f"Total Earnings: {earnings.count()}")
for e in earnings:
    print(f"  - {e.payroll.staff}: {e.earnings_type} = {e.amount}")

# Deductions
print("\n[DEDUCTIONS]")
deductions = Deductions.objects.all()
print(f"Total Deductions: {deductions.count()}")
for d in deductions:
    print(f"  - {d.payroll.staff}: {d.deduction_type} = {d.amount}")

# Salary Advances
print("\n[SALARY ADVANCES]")
advances = SalaryAdvance.objects.all()
print(f"Total Salary Advances: {advances.count()}")
for a in advances:
    print(f"  - {a.staff}: {a.amount} (Status: {a.status}, Reason: {a.reason})")

print("\n" + "="*80)
print("DATABASE AUDIT COMPLETE")
print("="*80 + "\n")
