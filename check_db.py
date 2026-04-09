import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from staff_management.models import Staff, StaffCategory

User = get_user_model()

print("="*60)
print("DATABASE DIAGNOSTIC REPORT")
print("="*60)

print("\n📋 USERS:")
print(f"Total: {User.objects.count()}")
for user in User.objects.all():
    print(f"  - {user.username} ({user.role})")

print("\n📋 STAFF CATEGORIES:")
print(f"Total: {StaffCategory.objects.count()}")
for cat in StaffCategory.objects.all():
    print(f"  - {cat.name}")

print("\n📋 STAFF MEMBERS:")
print(f"Total: {Staff.objects.count()}")
for staff in Staff.objects.all()[:10]:
    print(f"  - {staff.first_name} {staff.last_name} ({staff.staff_id})")

print("\n" + "="*60)
