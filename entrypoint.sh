#!/bin/bash
set -e

# Initialize database with sample data if needed
echo "🔧 Initializing production database..."
python initialize_production.py

# Then start gunicorn
echo "▶️  Starting Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
