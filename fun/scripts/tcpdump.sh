#!/bin/sh

# trace memcache request
#========================
#tcpdump -n -vvxXs 1500 -i eth0 'port 11211 and tcp[13] & 8 = 8'
#tcpdump -n -vvvAs 1500 -i eth0 'port 11211 and (tcp[13] & 8 = 8 or tcp[13] & 2 != 0 or tcp[13] & 16 != 0)'
tcpdump -n -vvvAs 1500 -i eth0 'port 11211 and tcp[13] & 8 = 8'
tcpdump -n -vvvAs 1500 -i eth0 '(dst port 11211 or dst port 11212 or dst port 11213)'

# 统计一下各种mongodb查询的情况 
#========================
tcpdump -vvvAs 1500 -n 'dst port 27017 and tcp[13] & 8 = 8' | grep --color royal | perl -ne '/^.{28}([^.]+\.[^.]+)(.+)/; print "$1\n";' > /mnt/logs/mongo.log 
cat /mnt/logs/mongo.log | cut -d'.' -f2 | sort | uniq -c | sort -nr 

# find dup tcp handshake sync
# the '-S' above which keeps sequence numbers intact(absolute instead of relative sequence number)
# this will be helpful to troubleshoot issues if some retransmits are found
# will write the logs to a pcap file conn.pcap, which can be analyzed in wireshark
#========================
tcpdump -w conn.pcap -Svvni eth0 'tcp[13]&7!=0 and (dst port 11211 or dst port 11212 or dst port 11213)'

# 只查看数据长度大于100的包
tcpdump -vvvAs 1500 -n 'port 27017 and tcp[13] & 8 = 8 and greater 100'


# less length
# 如果数据包的长度比length 小或等于length, 则与此对应的条件表达式为真. 这与'len <= length' 的含义一致.

# greater length
# 如果数据包的长度比length 大或等于length, 则与此对应的条件表达式为真. 这与'len >= length' 的含义一致.
tcpdump -nn -s0 -A 'port 10123 and greater 1500'
