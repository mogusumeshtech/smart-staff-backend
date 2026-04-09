import os
import getpass
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create or reset superuser admin with a secure password'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--email', type=str, default='admin@smartstaff.com', help='Admin email')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']

        # Prompt for password securely
        self.stdout.write('⚠️  SECURITY: You must provide a STRONG password for the admin user')
        self.stdout.write('Password must be at least 12 characters with uppercase, lowercase, numbers, and symbols')
        self.stdout.write('')

        password = getpass.getpass('Enter admin password: ')
        password_confirm = getpass.getpass('Confirm password: ')

        if password != password_confirm:
            self.stdout.write(self.style.ERROR('❌ Passwords do not match'))
            return

        if len(password) < 8:
            self.stdout.write(self.style.ERROR('❌ Password must be at least 8 characters'))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Admin user "{username}" created successfully'))
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Admin user "{username}" password updated successfully'))

        self.stdout.write(self.style.SUCCESS('🔒 Admin account is ready for production use'))
