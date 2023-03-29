#!/bin/bash

OPENCONNECT_PID=""
RUNNING=""
VPN_PASS=$1
VPN_USER=$2
VPN=$3

function checkOpenconnect {
    ps -p $OPENCONNECT_PID &> /dev/null
    RUNNING=$?

    #echo $RUNNING &>> reconnect.log
}

function startOpenConnect {
    echo $VPN_PASS |  openconnect -u $VPN_USER --passwd-on-stdin --servercert pin-sha256:ZEuEQV3tJ7MBbqWuaki2wEg3eaj+kyWJ7lbWkcSc0AU=  $VPN  & OPENCONNECT_PID=$!
#--servercert pin-sha256:ZEuEQV3tJ7MBbqWuaki2wEg3eaj+kyWJ7lbWkcSc0AU=
    echo $OPENCONNECT_PID
} &> /dev/null 
#echo $1
#echo $2
#echo $3
startOpenConnect
