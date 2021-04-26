#!/bin/bash

# Create runtime context directory
mkdir -p /run/sshd
/usr/sbin/sshd -D
