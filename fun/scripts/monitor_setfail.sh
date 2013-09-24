#!/bin/sh
checkpoint=13799703417821
while [ 1 ]; do
	lasterror=`cat /mnt/funplus/logs/fp_rstory/history/cache_set_fail_2013092* | grep '^us,'|cut -d',' -f2|sort|tail -1`
	echo $lasterror
	if [ $lasterror != $checkpoint ]; then
		echo -ne "\a"
	fi

	sleep 5
done
