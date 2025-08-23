#!/bin/bash
set -e

cd ordermanager
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn ordermanager.wsgi:application --bind 0.0.0.0:8000
fi