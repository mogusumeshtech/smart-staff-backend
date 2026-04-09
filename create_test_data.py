#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from staff_management.models import Staff, StaffCategory, Designation, Department

# Clean and create test data (delete in correct order to avoid foreign key issues)
Staff.objects.all().delete()
Designation.objects.all().delete()
Department.objects.all().delete()
StaffCategory.objects.all().delete()

# Create Masters
category = StaffCategory.objects.create(name="Teaching", description="Teaching Staff", is_active=True)
desig = Designation.objects.create(name="Teacher", category=category, salary_scale=30000.00, is_active=True)
dept = Department.objects.create(name="Academic", description="Academic Department", is_active=True)

# Create Staff
staff = Staff.objects.create(
    staff_id="TEST001",
    first_name="John",
    last_name="Doe",
    email="john@test.com",
    phone_number="1234567890",
    date_of_birth="1990-01-01",
    gender="M",
    category=category,
    designation=desig,
    department=dept,
    date_of_joining="2020-01-01",
    status="active",
    basic_salary=50000.00,
    is_active=True
)

print(f"✅ Created staff: {staff.staff_id}")
print(f"✅ Category: {staff.category.name}")
print(f"✅ Designation: {staff.designation.name}")
print(f"✅ Department: {staff.department.name}")
print(f"✅ Salary: {staff.basic_salary}")
print(f"✅ Active: {staff.is_active}")
