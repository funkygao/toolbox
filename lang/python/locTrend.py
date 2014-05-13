#!/usr/bin/env python
'''show trends of LineOfCode by weeks'''

import subprocess

# show current dir git log stat num
cmd = 'git log --shortstat --since "%d weeks ago" --until "%d week ago" ./| grep "files\? changed" | awk \'{files+=$1; inserted+=$4; deleted+=$6} END {print "files", files, "inserted:", inserted, "deleted:", deleted}\''

YEAR = 3
for week in reversed(range(1, 52*YEAR)): # weekly contributions for 3 years in reverse order
    parts = subprocess.Popen(cmd % (week+1, week), shell=True, stdout=subprocess.PIPE).stdout.read().split()
    if len(parts) != 6:
        continue

    files_changed, lines_added, lines_deleted = parts[1], parts[3], parts[5]
    print week, lines_added, lines_deleted

