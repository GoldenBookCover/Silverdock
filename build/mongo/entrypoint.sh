#!/bin/bash

echo "${MONGO_KEYFILE_TEXT}" > /etc/mongo-cluster.key
chown mongodb:mongodb /etc/mongo-cluster.key
chmod 400 /etc/mongo-cluster.key

exec /usr/local/bin/docker-entrypoint.sh "$@"
