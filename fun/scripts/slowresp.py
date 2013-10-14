#!/usr/bin/env python
'''dlog error_* analyzer'''

import json
import sys

for line in sys.stdin:
    area, ts, data = line.strip().split(',', 2)
    info = json.loads(data) # class, code, level, message, flash_version_client, batch_token
    ts = info['ts']
    uri = info['uri']
    uri = uri.split('?', 2)[0]
    print '%3s req:%3d db:%3d %s' % (area, ts['t2']-ts['t1'], ts['t3']-ts['t2'], uri)
