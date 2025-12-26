#!/bin/bash

version='1.0'

function _usage {
    echo "Usage:  $0 [OPT]"
    echo "        --version, -v: show version and exit"
    echo "        --help, -h: show help message and exit"
    echo "        --cluster-name=: \`_id\` in \`rs.initiate()\` (--replSet \${MONGO_CLUSTER_NAME})"
    echo "        --primary-server=: \`members.host\` in \`rs.initiate()\`"
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
    --cluster-name=*)
        cname=${1#--cluster-name=}
        echo "Creating cluster ${cname}"
        shift 1
        ;;
    --primary-server=*)
        thisserver=${1#--primary-server=}
        echo "Primary server ${thisserver}"
        shift 1
        ;;
    *)
        echo "Unknown option: $1"
        _usage
        ;;
esac

done

if [ -z $cname ] || [ -z $thisserver ]; then
    _usage
fi

mongosh --authenticationDatabase="$MONGO_INITDB_DATABASE" \
    --port="$MONGO_PORT" \
    --username="$MONGO_INITDB_ROOT_USERNAME" \
    --password="$MONGO_INITDB_ROOT_PASSWORD" \
    --eval \
"rs.initiate(
   {
      _id: '$cname',
      members: [
         { _id: 0, host: '$thisserver' }
      ]
   }
)"

