#!/bin/sh

ls /mnt/funplus/logs/fp_rstory/history/ | awk '{print $1}' | sed 's/[0-9]//g' | sort | uniq -c | sort -nr
