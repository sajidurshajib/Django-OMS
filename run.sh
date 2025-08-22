#!/bin/bash

# Project directory 
cd ordermanager

# Run migrations
# python manage.py migrate --noinput

# Collect static files (optional, for production)
# python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn ordermanager.wsgi:application --bind 0.0.0.0:8000

# python manage.py runserver 0.0.0.0:8000
