#!/bin/bash

# Start cronjob service(daemon)
service cron start

# Run django in interactive mode
if [ ${PYTHON_IS_PRODUCTION} = "true" ]; then
    uwsgi --ini uwsgi.ini
else
    python manage.py runserver 0.0.0.0:8000
fi