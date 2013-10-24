#!/usr/bin/env python
#encoding=utf-8

LOG_FILE = '/mnt/mongo/log/mongod.log'

THRESHOLD = 1000 # ms

def show_ms(logfile):
    for line in open(logfile):
        line = line.strip()
        if not line.endswith('ms'):
            continue
        msg, ts = line.rsplit(' ', 1)
        ts = int(ts.strip('ms'))
        if ts > THRESHOLD:
            print ts, msg

if __name__ == '__main__':
    show_ms(LOG_FILE)
