#!/bin/bash
usage(){
    echo "Usage: $0 (us|th|fr|de|ae|nl) (mongo|web|proxy|cache|log) [CMD]" >&2
}

hostlist=$(hosts | grep $1,$2 | cut -d',' -f3|awk '$1 !~ /^$/ {host = $1; if(FNR == 1){list[length(list)+1] = host}else{list[length(list)+1] = ","host}}END{ for(k=1;k<=length(list);k++){printf list[k]}}')

if [ "$#" -eq 0 ];then
    usage
    exit
fi

echo $hostlist
echo
pdsh -b -R ssh -l root -u 10 -w $hostlist $3

