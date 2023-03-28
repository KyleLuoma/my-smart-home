#!/bin/bash

status=`curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/gettemp`
echo `date` $status >> crash_checks.log

if [ "$status" -ne "200" ]
then
       # Take any appropriate recovery action here.
	echo "webserver seems down, restarting." >> check.log
	start-server-bg.sh norecovery
fi