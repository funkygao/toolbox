#!/bin/sh

# trace memcache request
#========================
#tcpdump -n -vvxXs 1500 -i eth0 'port 11211 and tcp[13] & 8 = 8'
#tcpdump -n -vvvAs 1500 -i eth0 'port 11211 and (tcp[13] & 8 = 8 or tcp[13] & 2 != 0 or tcp[13] & 16 != 0)'
tcpdump -n -vvvAs 1500 -i eth0 'port 11211 and tcp[13] & 8 = 8'

# 统计一下各种mongodb查询的情况 
#========================
tcpdump -vvvAs 1500 -n 'dst port 27017 and tcp[13] & 8 = 8' | grep --color royal | perl -ne '/^.{28}([^.]+\.[^.]+)(.+)/; print "$1\n";' > /mnt/logs/mongo.log 
cat /mnt/logs/mongo.log | cut -d'.' -f2 | sort | uniq -c | sort -nr 

# find dup tcp handshake sync
# the '-S' above which keeps sequence numbers intact
# this will be helpful to troubleshoot issues if some retransmits are found
#========================
tcpdump -Svvni eth0 'tcp[13]&7!=0 and (dst port 11211 or dst port 11212 or dst port 11213)'
