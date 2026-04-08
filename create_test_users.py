#!/usr/bin/env python
"""Create test users"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import CustomUser

users_data = [
    {'username': 'hrmanager', 'email': 'hr@smartstaff.local', 'password': 'hr123'},
    {'username': 'finance', 'email': 'finance@smartstaff.local', 'password': 'finance123'},
    {'username': 'principal', 'email': 'principal@smartstaff.local', 'password': 'principal123'},
]

print("Creating test users...\n")

for user_data in users_data:
    if not CustomUser.objects.filter(username=user_data['username']).exists():
        CustomUser.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            is_active=True,
            is_staff=True
        )
        print(f"✓ {user_data['username']} / {user_data['password']}")
    else:
        print(f"✓ Already exists: {user_data['username']}")

print("\nAll accounts ready for testing!")
