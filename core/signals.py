from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    """Create admin user after migrations"""
    if User.objects.filter(username='admin').exists():
        # Update existing admin password
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        print("[OK] Admin user password updated: admin123")
    else:
        # Create new admin user
        User.objects.create_superuser(
            username='admin',
            email='admin@smartstaff.com',
            password='admin123'
        )
        print("[OK] Admin user created: username=admin, password=admin123")
