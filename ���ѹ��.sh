#!/bin/bash

while [ true ]
do
logTime=`date`
load=`w | grep "load" `
echo "$logTime $load"
sleep 120
done
