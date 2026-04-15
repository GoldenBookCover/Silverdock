#!/bin/bash

# Start cronjob service(daemon)
if [ "x${ENABLE_CRONJOB}" = "xtrue" ]; then
    service cron start
fi

# Run django in interactive mode
if [ "x${PYTHON_IS_PRODUCTION}" = "xtrue" ]; then
    _cmd="uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"
else
    _cmd="uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
fi

exec gosu www-data $_cmd
