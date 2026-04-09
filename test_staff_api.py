#!/usr/bin/env python
"""Test staff creation through API"""

import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Get admin user
admin_user = User.objects.filter(username='admin').first()
if not admin_user:
    print("❌ Admin user not found!")
    exit(1)

# Generate token for admin
refresh = RefreshToken.for_user(admin_user)
access_token = str(refresh.access_token)

print("✅ Admin token generated")
print(f"Token: {access_token[:50]}...")

# API endpoint
api_url = "http://localhost:8000/api/v1/staff/"

# Test staff data
staff_data = {
    "staff_id": "TEST_001",
    "first_name": "Test",
    "last_name": "Staff",
    "email": "test@school.com",
    "phone_number": "+254712345678",
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "category": 1,  # TEACHING
    "designation": 1,
    "department": 1,
    "date_of_joining": "2024-01-01",
    "status": "active",
    "basic_salary": 50000.00,
    "permanent_address": "123 Main St"
}

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

print("\n📤 Sending POST request to create staff...")
print(f"URL: {api_url}")
print(f"Data: {json.dumps(staff_data, indent=2)}")

try:
    response = requests.post(api_url, json=staff_data, headers=headers, timeout=5)
    print(f"\n✅ Response Status: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 201:
        print("\n✨ SUCCESS! Staff created!")
    else:
        print(f"\n❌ ERROR: {response.text}")

except Exception as e:
    print(f"\n❌ REQUEST FAILED: {str(e)}")
