#!/bin/bash

# Start cronjob service(daemon)
if [ "x${ENABLE_CRONJOB}" = "xtrue" ]; then
    service cron start
fi

# Run your app in interactive mode
exec $@
