#!/bin/bash

for i in "$@"; do
    echo "$i REJECT" >> /etc/postfix/sender_access
done

postmap hash:/etc/postfix/sender_access
