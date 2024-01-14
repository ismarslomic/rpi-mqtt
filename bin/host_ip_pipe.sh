#!/bin/bash

############################################
### https://stackoverflow.com/a/63719458 ###
############################################

if [ ! -p "/tmp/host_ip_pipe" ]; then
    mkfifo "/tmp/host_ip_pipe"
fi

while true; do cat /proc/net/tcp > "/tmp/host_ip_pipe"; sleep 0.5; done;
