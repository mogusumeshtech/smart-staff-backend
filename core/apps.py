from django.apps import AppConfig
import sys

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals  # noqa

        # Django 4.2 + Python 3.14 compatibility fix
        # Fixes: AttributeError: 'super' object has no attribute 'dicts'
        if sys.version_info >= (3, 14):
            try:
                from django.template.context import Context
                original_copy = Context.__copy__

                def patched_copy(self):
                    # Create instance without calling __init__
                    duplicate = self.__class__.__new__(self.__class__)
                    duplicate.dicts = self.dicts[:]
                    return duplicate

                Context.__copy__ = patched_copy
            except Exception as e:
                print(f"Warning: Could not apply Django 3.14 compatibility patch: {e}")
