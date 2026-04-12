import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Create credentials
username = 'admin'
email = 'admin@smartstaff.local'
password = 'SmartStaff@2026Secure!'  # Strong password

try:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': 'System',
            'last_name': 'Admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )

    if created:
        user.set_password(password)
        user.save()
        print("✅ ADMIN USER CREATED")
    else:
        user.set_password(password)
        user.save()
        print("✅ ADMIN USER UPDATED")

    print(f"\n📋 LOGIN CREDENTIALS:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: {email}")
    print(f"\n🔐 SECURITY STATUS:")
    print(f"   Staff Account: Yes")
    print(f"   Superuser: Yes")
    print(f"   API Access: Full")

except Exception as e:
    print(f"❌ Error: {e}")
