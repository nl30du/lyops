#!/bin/bash
LoginUser=$1
FingerPrint=$2
for ((retry=1;retry<=3;retry++));
do
        curl --connect-timeout 3 "http://192.168.146.128:8080/ops/sshkey/get?fp=$FingerPrint&loginuser=$LoginUser&p=LS" 2>/dev/null
        if [ $? -eq 0 ];then
                exit;
        else
                sleep 1
                continue
        fi
done
