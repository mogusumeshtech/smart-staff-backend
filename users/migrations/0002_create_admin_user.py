from django.db import migrations
from django.contrib.auth import get_user_model

def create_admin_user(apps, schema_editor):
    """Create default admin user if it doesn't exist"""
    User = get_user_model()

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@smartstaff.local',
            password='SmartStaff@2026Secure!',
            first_name='System',
            last_name='Admin',
        )
        print("[MIGRATION] Admin user created successfully")
    else:
        # Update password in case it changed
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('SmartStaff@2026Secure!')
        admin_user.save()
        print("[MIGRATION] Admin user already exists, password updated")

def reverse_admin_user(apps, schema_editor):
    """Don't delete admin user on reverse - it's unsafe"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, reverse_admin_user),
    ]
