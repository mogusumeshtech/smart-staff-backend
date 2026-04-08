import os
import sys

# CRITICAL: Patch MUST load before ANY Django import
# This fixes Python 3.14 + Django 4.2 template rendering issues
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from config.django_init import apply_python314_django42_fixes
    apply_python314_django42_fixes()
except Exception as e:
    import traceback
    print(f"[WSGI] Failed to load django_init: {e}")
    traceback.print_exc()

# NOW safe to import Django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
