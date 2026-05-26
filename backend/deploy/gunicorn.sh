#!/usr/bin/env bash

echo 'Starting Gunicorn server...'

python manage.py migrate
python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:8000 --workers 4 shoonya_backend.wsgi --timeout 300

