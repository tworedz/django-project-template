#!/bin/sh

set -o errexit

#timeout 60 sh -c "until nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do sleep 1; done"

# Startup commands
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn core.wsgi:application -b 0.0.0.0:8000 --reload -w 4 --timeout 1200
