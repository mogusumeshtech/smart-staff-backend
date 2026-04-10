#!/bin/bash

echo "🚀 SMART STAFF API - Container Starting..."
echo ""

# Try migrations - don't fail if it doesn't work on first run
echo "📦 Running migrations..."
python manage.py migrate --noinput 2>/dev/null || echo "⚠️  Migrations skipped (DB might not exist yet)"

# Try collecting static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || echo "⚠️  Static files collection skipped"

# Start gunicorn
PORT=${PORT:-8000}
echo "▶️  Starting Gunicorn on port ${PORT}..."
echo ""

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
