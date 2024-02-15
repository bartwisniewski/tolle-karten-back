#!/bin/sh

set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000

python -m celery -A tkbproj worker
