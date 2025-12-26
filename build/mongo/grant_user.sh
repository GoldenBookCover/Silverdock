#!/bin/bash

version='1.0'

function _usage {
    echo "Usage:  $0 [OPT]"
    echo "        --version, -v: show version and exit"
    echo "        --help, -h: show help message and exit"
    echo "        --username=: user name to grant"
    echo "        --password=: user pasword to grant"
    echo "        --dbname=: database to grant"
    exit 0
}

# Parameters
while [ ! -z $1 ]; do

case $1 in
    --version|-v)
        echo "version $version"
        exit 0
        ;;
    --help|-h)
        _usage
        ;;
    --username=*)
        username=${1#--username=}
        shift 1
        ;;
    --password=*)
        password=${1#--password=}
        shift 1
        ;;
    --dbname=*)
        dbname=${1#--dbname=}
        shift 1
        ;;
    *)
        echo "Unknown option: $1"
        _usage
        ;;
esac

done

if [ -z $username ] || [ -z $password ] || [ -z $dbname ]; then
    _usage
fi

mongosh --authenticationDatabase="$MONGO_INITDB_DATABASE" \
    --port="$MONGO_PORT" \
    --username="$MONGO_INITDB_ROOT_USERNAME" \
    --password="$MONGO_INITDB_ROOT_PASSWORD" \
    --eval \
"db.getSiblingDB('admin').createUser({
  user: '$username',
  pwd: '$password',
  roles: [
    { role: 'readWrite', db: '$dbname' },
    { role: 'dbAdmin', db: '$dbname' }
  ]
})"

