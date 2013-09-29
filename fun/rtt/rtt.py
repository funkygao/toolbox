#!/usr/bin/env python
'''Calc the rtt inside aws intranet'''

import sys
from collections import defaultdict
import datetime

SRC = '10.130.113.120'

def time_diff(t1, t2):
    t1 = datetime.datetime.strptime(t1, "%H:%M:%S.%f")
    t2 = datetime.datetime.strptime(t2, "%H:%M:%S.%f")
    delta = t2 - t1 if t2 > t1 else t1 - t2
    return abs(delta.microseconds/1000.) # ms


def main(tcpdumpfile):
    data = defaultdict(list)
    for l in open(tcpdumpfile):
        l = l.strip()
        parts = l.split()
        ts, src, dst = parts[0], parts[2], parts[4].strip(':')
        if SRC in src:
            # client -> server
            data[src + '-' + dst].append(ts)
        else:
            # server -> client
            data[dst + '-' + src].append(ts)

    count, total = 0, .0
    for session, ts in data.iteritems():
        if len(ts) == 2:
            count += 1
            diff = time_diff(ts[1], ts[0])
            total += diff
            print session, str(diff) + 'ms'

    print '\navg:', total/count, 'ms'

if __name__ == '__main__':
    main(sys.argv[1])

