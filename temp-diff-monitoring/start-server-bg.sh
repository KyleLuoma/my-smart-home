#!/bin/bash

nohup flask run --host 0.0.0.0 > l.txt 2>&1 &

if [ "$1" != "norecovery" ]
then
    crash-recovery.sh
fi