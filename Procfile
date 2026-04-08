web: gunicorn config.wsgi
release: sh -c 'python manage.py migrate && python seed_admin.py'
