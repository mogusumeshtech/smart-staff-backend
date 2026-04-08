import os
import sys

# DO NOT DELETE - Critical compatibility fixes for Python 3.14
# Must be loaded before Django initializes
try:
    from config.django_init import apply_python314_django42_fixes
    apply_python314_django42_fixes()
except Exception as e:
    import traceback
    traceback.print_exc()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
