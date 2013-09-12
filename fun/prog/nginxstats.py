#!/usr/bin/env python

import re
import sys
import time
import datetime
import urllib2 as urllib

TIME_SLEEP = 2

COLOR_RED = "\033[33;31m"
COLOR_GREEN = "\033[33;32m"
COLOR_YELLOW = "\033[33;33m"
COLOR_RESET = "\033[m"

RPS_BAR_STEP = 50
RPS_ALERT, RPS_WARN = 800/RPS_BAR_STEP, 600/RPS_BAR_STEP

def get_data(url):
    data = urllib.urlopen(url)
    data = data.read()
    result = {}

    match1 = re.search(r'Active connections:\s+(\d+)', data)
    match2 = re.search(r'\s*(\d+)\s+(\d+)\s+(\d+)', data)
    match3 = re.search(r'Reading:\s*(\d+)\s*Writing:\s*(\d+)\s*'
        'Waiting:\s*(\d+)', data)
    if not match1 or not match2 or not match3:
        raise Exception('Unable to parse %s' % url)

    result['connections'] = int(match1.group(1))

    result['accepted'] = int(match2.group(1))
    result['handled'] = int(match2.group(2))
    result['requests'] = int(match2.group(3))

    result['reading'] = int(match3.group(1))
    result['writing'] = int(match3.group(2))
    result['waiting'] = int(match3.group(3))

    result['now'] = time.time()

    return result

def main():
    url = sys.argv[1]
    print '=' * 5, url, '=' * 5, '\n'
    delta, prev, total, count = 0, None, None, 0
    try:
        while True:
            data = get_data(url)
            if prev:
                result = print_stat(prev, data)
                if total is None:
                    total = list(result)
                else:
                    for i, v in enumerate(result):
                        total[i] += v
                count += 1
            else:
                print_head()
            prev = data
            time.sleep(TIME_SLEEP)
    except KeyboardInterrupt:
        if total:
            print_foot(total, count)


def print_foot(total, count):
    total = [v / count for v in total]
    print '-------- -------- ---------- ---------- ----- ----- -----'
    print '%8s' % now_str(), '%8d %10.2f %10.2f %5d %5d %5d' % tuple(total)

def now_str():
    now = datetime.datetime.now()
    return '%02d:%02d:%02d' % (now.hour, now.minute, now.second)

def print_head():
    print '%-8s %-8s %-10s %-5s %-5s %-5s %-10s %-20s' % (
        'Now', 'Conn', 'Conn/s', 'Read', 'Write', 'Wait', 'RPS', 'RPSbar')
    print '-------- -------- ---------- ----- ----- ----- ----------', '-' * 20

def rps_bar(rps):
    color = COLOR_GREEN
    if rps >= RPS_ALERT:
        color = COLOR_RED
    elif rps >= RPS_WARN:
        color = COLOR_YELLOW
    return color + '#' * rps + COLOR_RESET

def print_stat(prev, data):
    result = (
        data['connections'],
        float(data['accepted'] - prev['accepted']) / (data['now'] - prev['now']),
        data['reading'],
        data['writing'],
        data['waiting'],
        float(data['requests'] - prev['requests']) / (data['now'] - prev['now']),
        )

    print '%8s' % now_str(), '%8d %10.2f %5d %5d %5d %10.2f' % result, rps_bar(int(result[5]/50))
    return result
        

if __name__ == '__main__':
    main()
