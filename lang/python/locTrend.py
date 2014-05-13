#!/usr/bin/env python
'''show trends of LineOfCode by weeks'''

import subprocess

# show current dir git log stat num
cmd = 'git log --shortstat --since "%d weeks ago" --until "%d week ago" ./| grep "files\? changed" | awk \'{files+=$1; inserted+=$4; deleted+=$6} END {print "files", files, "inserted:", inserted, "deleted:", deleted}\''

for i in range(1, 30):
    log = subprocess.Popen(cmd % (i+1, i), shell=True, stdout=subprocess.PIPE).stdout.read()
    parts = log.split()
    if len(parts) != 6:
        continue
    files_changed, lines_added, lines_deleted = parts[1], parts[3], parts[5]
    print lines_added, lines_deleted

