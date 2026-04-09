from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def on_migrations_complete(sender, **kwargs):
    """Post-migration hook - admin user must be created manually via management command"""
    pass

