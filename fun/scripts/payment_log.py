#!/usr/bin/env python
'''dlog payment_* analyzer'''

import json
import sys
import locale
from collections import defaultdict

total, levels, items = defaultdict(int), defaultdict(int), defaultdict(int)

for line in sys.stdin:
    area, ts, data = line.strip().split(',', 2)
    info = json.loads(data)
    t, data = info['type'], info['data']
    if t != 'OK':
        print t
        continue

    total[data['currency']] += int(data['amount'])
    levels[data['level']] += 1
    items[data['item']] += 1

def print_ordered_result(title, d, threshold=None):
    print '*' * 10, title, '*'*10
    r = sorted( ((v, k) for k, v in d.iteritems()), reverse=True)
    for k, v in r:
        if threshold is not None and k < threshold:
            break
        # print "%10s %s" % (v, "{:,d}".format(k)) # only works above python2.7
        print "%10s %s" % (v, locale.format("%d", k, grouping=True))
    print

locale.setlocale(locale.LC_ALL, '')
print_ordered_result('mongy', total)
print_ordered_result('level', levels, 100)
print_ordered_result('type', items)
