#!/bin/bash

#Define cleanup procedure
cleanup() {
    echo "Container stopped, performing cleanup..."
    gosu tomcat /usr/local/tomcat/bin/shutdown.sh
    kill `cat /run/this_container.pid`
}

#Trap SIGTERM
trap 'cleanup' SIGTERM

#Execute a command
gosu tomcat /usr/local/tomcat/bin/startup.sh

tail -n 0 -f /usr/local/tomcat/logs/catalina.out &

echo $! > /run/this_container.pid

#Wait
wait `cat /run/this_container.pid`

