#!/bin/bash

# Start cronjob service(daemon)
if [ "x${ENABLE_CRONJOB}" = "xtrue" ]; then
    service cron start
fi

# Run django in interactive mode
if [ "x${PYTHON_IS_PRODUCTION}" = "xtrue" ]; then
    _cmd="uwsgi --ini uwsgi.ini"
else
    _cmd="python manage.py runserver 0.0.0.0:8000"
fi

exec gosu www-data $_cmd
