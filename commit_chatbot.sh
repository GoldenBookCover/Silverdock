#!/bin/bash

for i in \
  mongo \
  php-worker \
  workspace \
  php-fpm \
  laravel-echo-server \
; do
  docker tag chatbot_t-$i:latest mccarthf/chatbot-$i:latest
  docker push mccarthf/chatbot-$i:latest
done

