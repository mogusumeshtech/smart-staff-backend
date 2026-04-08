#!/usr/bin/env python
import os
import sys

# CRITICAL: Apply compatibility patches BEFORE Django initializes
sys.path.insert(0, os.path.dirname(__file__))
try:
    from config.django_init import apply_python314_django42_fixes
    apply_python314_django42_fixes()
except Exception as e:
    print(f"Warning: django_init exception: {e}")

import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
