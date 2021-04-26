#!/bin/bash

# Start cronjob service(daemon)
service cron start

# Run php-fpm in interactive mode
php-fpm
