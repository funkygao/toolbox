#!/usr/bin/env python

import time
import sys
import json
import urllib2 as urllib
import random

COLOR_RED = "\033[33;31m"
COLOR_RESET = "\033[m"
ALARM_MSG = 'time drift'

URL_FMT = 'http://royal-%s.socialgamenet.com/time.php'
TIME_DIFF_THRESHOLD = 1
N, STEP = 200, 10

def step_hint(n, i):
    bar = i * 80 / n
    space = 80 - bar
    print '[' + bar * '*' + space * ' ' + ']'

def get_timestamp(url):
    url += '?t=' + str(random.random())
    begin = time.time()
    js = urllib.urlopen(url).read()
    rtt = time.time() - begin
    t = json.loads(js)
    return float(t['time']), rtt

def main(area):
    url = URL_FMT % area
    last = 0.
    for i in range(N):
        if i>0 and i % STEP == 0:
            step_hint(N, i)
        t, rtt = get_timestamp(url)
        diff = t - last - rtt
        if last > 0 and abs(diff) > TIME_DIFF_THRESHOLD:
            print i, COLOR_RED + ALARM_MSG + COLOR_RESET + ': [', last, t, ']', diff
        last = t

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s area' % sys.argv[0]
        sys.exit(1)

    main(sys.argv[1])
    
