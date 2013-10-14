#!/bin/bash

# script_filename='mongo_db_size.js'
script_filename='user.js'

list=`php -r "\\$a = require '/www/config/us/database.php'; foreach (\\$a as \\$b => \\$c) { \\$b = substr(\\$b, 2); if (\\$b < 1) { continue; }; echo \\$b.'|'.\\$c['host'].'\n'; };"`

# server_list=(`echo -e $list`)
server_list=(`echo -e $list | tail -n 18 | head -n 10`)

for server in "${server_list[@]}"
do

	tmp=(`echo $server | tr "|" " "`)

	server_id=${tmp[0]}
	server_ip=${tmp[1]}

	echo
	echo $server_id": "$server_ip
	echo

	scp $script_filename $server_ip':/tmp/'

	ssh $server_ip "mongo royal_"$server_id" /tmp/"$script_filename > 'server_output/'$server_id'.txt'

	# ssh -q $server "ls"

done
