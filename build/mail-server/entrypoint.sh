#!/bin/bash

service rsyslog start
service postfix start
service spamassassin start
service opendkim start
service dovecot start

tail -f /var/log/mail.log
