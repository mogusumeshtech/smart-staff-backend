#!/bin/bash
set -e

echo "Starting SMART STAFF API..."

# Set Python to not write bytecode
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Get port from environment or default to 8000
PORT=${PORT:-8000}

# Try migrations (non-fatal if DB not configured yet)
python manage.py migrate --noinput 2>/dev/null || true

# Collect static files (optional)
python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Start gunicorn
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:${PORT} \
  --workers 2 \
  --worker-class sync \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -

