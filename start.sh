#!/bin/bash
# Django 4.2 + Python 3.14 compatibility initialization

# Apply Python 3.14 context copy fix at the C library level
export PYTHONPATH="/opt/render/project/src/config:$PYTHONPATH"

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput --clear

# Start Gunicorn with Django properly initialized
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
