#!/bin/bash
while [ true ]
do
#sleep 2 seconds

DATE=`date +%Y%m%d%H%M`
#awk '{print "jstack " $1 ">jstack.log$DATE"}'
`jps | grep "Main" | awk '{print "jstack " $1 ">jstack.log'$DATE'"}' | sh`
sleep 120
done
