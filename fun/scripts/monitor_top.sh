#!/bin/sh
while [ 1 ]; do
	top -n 1 -b >> /mnt/logs/top.out
	sleep 20
done
