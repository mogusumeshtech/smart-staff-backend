#!/bin/bash
# Load sample data if database is empty
python manage.py load_sample_data

# Then start gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
