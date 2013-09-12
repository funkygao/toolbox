#!/usr/bin/env python
#encoding=utf-8

import re
import sys
import time
import datetime
import urllib2 as urllib
import socket

TIME_SLEEP = 2

COLOR_RED = "\033[33;31m"
COLOR_GREEN = "\033[33;32m"
COLOR_YELLOW = "\033[33;33m"
COLOR_RESET = "\033[m"

RPS_BAR_STEP = 50
RPS_BAR_MAX_LEN = 50
RPS_ALERT, RPS_WARN = 800/RPS_BAR_STEP, 600/RPS_BAR_STEP

NGINX_STATUS = '/nginx_status'

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

def get_ips_of_domain(domain):
    ''' -> [ip1, ip2]'''
    r = socket.gethostbyname_ex(domain)
    return r[2]

def main():
    domain = sys.argv[1]
    ips = get_ips_of_domain(domain)
    run(ips[0])

def run(ip):
    url = 'http://' + ip + NGINX_STATUS
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


def now_str():
    now = datetime.datetime.now()
    return '%02d:%02d:%02d' % (now.hour, now.minute, now.second)

def rps_bar(rps):
    if rps > RPS_BAR_MAX_LEN:
        rps = RPS_BAR_MAX_LEN

    color = COLOR_GREEN
    if rps >= RPS_ALERT:
        color = COLOR_RED
    elif rps >= RPS_WARN:
        color = COLOR_YELLOW
    return color + '#' * rps + COLOR_RESET

def print_head():
    print '%-8s %-8s %-10s %-5s %-5s %-5s %-10s %-20s' % (
        'Now', 'Conn', 'Conn/s', 'Read', 'Write', 'Wait', 'RPS', 'RPSbar')
    print '-------- -------- ---------- ----- ----- ----- ----------', '-' * 20

def print_foot(total, count):
    total = [v / count for v in total]
    print '-------- -------- ---------- ----- ----- ----- ----------', '-' * 18 
    print '%8s' % now_str(), '%8d %10.2f %5d %5d %5d %10.2f' % tuple(total), rps_bar(int(total[5]/RPS_BAR_STEP))

def print_stat(prev, data):
    result = (
        data['connections'],
        float(data['accepted'] - prev['accepted']) / (data['now'] - prev['now']),
        data['reading'],
        data['writing'],
        data['waiting'],
        float(data['requests'] - prev['requests']) / (data['now'] - prev['now']),
        )

    print '%8s' % now_str(), '%8d %10.2f %5d %5d %5d %10.2f' % result, rps_bar(int(result[5]/RPS_BAR_STEP))
    return result
        

if __name__ == '__main__':
    main()
