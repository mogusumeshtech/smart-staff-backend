import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Create credentials
username = 'admin'
email = 'admin@smartstaff.local'
password = 'SmartStaff@2026Secure!'

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
        print("[CREATED] ADMIN USER CREATED")
    else:
        user.set_password(password)
        user.save()
        print("[UPDATED] ADMIN USER UPDATED")

    print("")
    print("LOGIN CREDENTIALS:")
    print("   Username: " + username)
    print("   Password: " + password)
    print("   Email: " + email)
    print("")
    print("SECURITY STATUS:")
    print("   Staff Account: Yes")
    print("   Superuser: Yes")
    print("   API Access: Full")

except Exception as e:
    print("[ERROR] " + str(e))
