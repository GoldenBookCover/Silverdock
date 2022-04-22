#!/bin/bash

# Create runtime context directory
mkdir -p /run/sshd
exec /usr/sbin/sshd -D
