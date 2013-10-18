#!/bin/bash
usage(){
    echo "Usage: $0 [us|th|fr|de|ae|nl] (mongo|web|proxy|cache|log) [CMD]" >&2
}

if [ "$#" -eq 0 ];then
    usage
    exit
fi

keyword=''
cmd=''
if [ "$#" -eq 3 ];then
	keyword="$1,$2"
	cmd="$3"
fi

if [ "$#" -eq 2 ];then
	keyword="$1"
	cmd="$2"
fi

if [ "$#" -eq 1 ];then
	keyword="$1"
fi

hostlist=$(/root/bin/cluster | grep $keyword | cut -d',' -f3|awk '$1 !~ /^$/ {host = $1; if(FNR == 1){list[length(list)+1] = host}else{list[length(list)+1] = ","host}}END{ for(k=1;k<=length(list);k++){printf list[k]}}')

RED="\033[33;31m"
GREEN="\033[33;32m"
YELLOW="\033[33;33m"
BLUE="\033[33;34m"
PURPLE="\033[33;35m"
RESET="\033[m"

echo -e "${GREEN}==============================================================================================${RESET}"
echo -e "${RED}$hostlist${RESET}"
echo -e "${GREEN}==============================================================================================${RESET}"
pdsh -b -R ssh -l root -u 10 -w $hostlist $cmd
