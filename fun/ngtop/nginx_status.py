#!/usr/bin/env python
#encoding=utf-8

import re
import sys
import time
import datetime
import urllib2 as urllib

TIME_SLEEP = 2

COLOR_RED = "\033[33;31m"
COLOR_GREEN = "\033[33;32m"
COLOR_YELLOW = "\033[33;33m"
COLOR_PURPLE = "\033[33;35m"
COLOR_BLUE = "\033[33;34m"
COLOR_LIGHT_CYAN = "\033[36;36m"
COLOR_RESET = "\033[m"

RPS_BAR_SYMBOL = 'o'
RPS_BAR_STEP = 60
RPS_BAR_MAX_LEN = 30
RPS_ALERT, RPS_WARN = 800/RPS_BAR_STEP, 600/RPS_BAR_STEP

NGINX_STATUS = '/nginx_status'

COLORS = [COLOR_BLUE, COLOR_PURPLE, COLOR_LIGHT_CYAN, COLOR_GREEN]

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

def run(ip, ipcolor):
    url = 'http://' + ip + NGINX_STATUS
    prev = None
    try:
        while True:
            data = get_data(url)
            if prev:
                result = print_stat(ipcolor, ip, prev, data)
            prev = data
            time.sleep(TIME_SLEEP)
    except KeyboardInterrupt:
        pass

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
    return color + RPS_BAR_SYMBOL * rps + COLOR_RESET

def print_stat(ipcolor, ip, prev, data):
    result = (
        data['connections'],
        float(data['accepted'] - prev['accepted']) / (data['now'] - prev['now']),
        data['reading'],
        data['writing'],
        data['waiting'],
        float(data['requests'] - prev['requests']) / (data['now'] - prev['now']),
        )

    color_format = COLORS[ipcolor] + "%16s" + COLOR_RESET
    print color_format % ip,
    print '%8s' % now_str(), '%8d %10.2f %5d %5d %5d %10.2f' % result, rps_bar(int(result[5]/RPS_BAR_STEP))
    sys.stdout.flush() # very important for popen to read my output!
    return result
        
def main():
    if len(sys.argv) < 3:
        ipcolor = 0
    else:
        ipcolor = int(sys.argv[2])
    ip = sys.argv[1]
    run(ip, ipcolor)

if __name__ == '__main__':
    main()
