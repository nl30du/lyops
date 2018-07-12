#!/bin/bash

export REALUSER=$1


if [ -z "$SSH_ORIGINAL_COMMAND" ] ;then
    #curl --connect-timeout 3 -d"username=$REALUSER&logintype=1" http://10.155.245.248/sshkey/report >/dev/null 2>&1
    cat /etc/motd
    exec bash -l
else
    #curl --connect-timeout 3 -d"username=$REALUSER&logintype=2" http://10.155.245.248/sshkey/report >/dev/null 2>&1
    # echo "bash[$$] [$SSH_CLIENT] [$USER:$REALUSER] $SSH_ORIGINAL_COMMAND" |nc -w1 -u 192.168.146.133 514
    SSH_CLIENT_IP=`echo ${SSH_CLIENT} | awk '{print $1}'`
    echo "pass ChK]$USER]$REALUSER]${SSH_CLIENT_IP}]1]pass]${SSH_ORIGINAL_COMMAND}" | nc -w1 192.168.146.133 514
    if [ -n "$SHELL" ] ;then
        exec bash -l -c "$SSH_ORIGINAL_COMMAND"
    else
        exec bash -l -c "$SSH_ORIGINAL_COMMAND"
    fi
fi
