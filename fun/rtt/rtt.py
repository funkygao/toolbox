#!/usr/bin/env python
'''Calc the rtt inside aws intranet'''

import sys

def main(tcpdumpfile):
    data = {}
    for l in open(tcpdumpfile):
        l = l.strip()
        parts = l.split()
        ts, src, dst = parts[0], parts[2], parts[4].strip(':')
        if data.get(src) is None:
            data[src] = []
        if data.get(dst) is None:
            data[dst] = []
        data[src].append(ts)
        data[dst].append(ts)

    print data
        


if __name__ == '__main__':
    main(sys.argv[1])

