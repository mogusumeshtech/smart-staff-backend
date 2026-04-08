#!/usr/bin/env python
import os
import sys
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

# Delete the migration history from the database
dbpath = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
try:
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM django_migrations')
    conn.commit()
    print("✓ Cleared migration history from database")
    conn.close()
except Exception as e:
    print(f"Note: Could not clear migrations (may not exist yet): {e}")

# Now setup Django and run migrations
django.setup()

from django.core.management import call_command

print("\nRunning migrations fresh...\n")
call_command('migrate', verbosity=2)

print("\n✓ Migrations complete!")
