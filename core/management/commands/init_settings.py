from django.core.management.base import BaseCommand
from core.models import SchoolSettings


class Command(BaseCommand):
    help = 'Initialize or update school settings with default values'

    def add_arguments(self, parser):
        parser.add_argument(
            '--school-name',
            type=str,
            default='St Elizabeth Igorera School',
            help='School name (default: St Elizabeth Igorera School)'
        )
        parser.add_argument(
            '--address',
            type=str,
            default='',
            help='School address'
        )
        parser.add_argument(
            '--timezone',
            type=str,
            default='Africa/Nairobi',
            help='Timezone (default: Africa/Nairobi)'
        )
        parser.add_argument(
            '--currency',
            type=str,
            default='KES',
            help='Currency code (default: KES)'
        )
        parser.add_argument(
            '--phone',
            type=str,
            default='',
            help='School phone number'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='',
            help='School email address'
        )

    def handle(self, *args, **options):
        # Get or create the singleton settings instance
        settings, created = SchoolSettings.objects.get_or_create(pk=1)

        # Update with provided values
        settings.school_name = options['school_name']
        settings.school_address = options['address']
        settings.timezone = options['timezone']
        settings.currency = options['currency']
        settings.phone = options['phone']
        settings.email = options['email']
        settings.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created school settings for "{settings.school_name}"')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Updated school settings for "{settings.school_name}"')
            )

        self.stdout.write(self.style.SUCCESS('School Settings Initialized:'))
        self.stdout.write(f'  School Name: {settings.school_name}')
        self.stdout.write(f'  Address: {settings.school_address}')
        self.stdout.write(f'  Timezone: {settings.timezone}')
        self.stdout.write(f'  Currency: {settings.currency}')
        self.stdout.write(f'  Phone: {settings.phone}')
        self.stdout.write(f'  Email: {settings.email}')
