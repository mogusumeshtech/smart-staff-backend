import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django 4.2 + Python 3.14 compatibility patch
# Fixes AttributeError in template context copying
import django.template.context as ctx_module
if sys.version_info >= (3, 14):
    try:
        original_copy = ctx_module.Context.__copy__
        def patched_copy(self):
            duplicate = super(ctx_module.Context, self).__copy__()
            duplicate.dicts = self.dicts[:]
            return duplicate
        ctx_module.Context.__copy__ = patched_copy
    except Exception:
        pass

application = get_wsgi_application()
