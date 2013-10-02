#!/usr/bin/env python
'''dlog payment_* analyzer'''

import json
import sys
from collections import defaultdict

total, levels, items = defaultdict(int), defaultdict(int), defaultdict(int)

for line in sys.stdin:
    locale, ts, data = line.strip().split(',', 2)
    info = json.loads(data)
    t, data = info['type'], info['data']
    if t != 'OK':
        print t
        continue

    total[data['currency']] += int(data['amount'])
    levels[data['level']] += 1
    items[data['item']] += 1

def print_ordered_result(title, d):
    print '*' * 10, title, '*'*10
    r = sorted( ((v, k) for k, v in d.iteritems()), reverse=True)
    for k, v in r:
        print "%10s %s" % (v, "{:,.2f}".format(k))
    print

print_ordered_result('mongy', total)
print_ordered_result('level', levels)
print_ordered_result('type', items)
