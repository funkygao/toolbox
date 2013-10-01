#!/usr/bin/env python
'''dlog error_* analyzer'''

import json
import sys

for line in sys.stdin:
    locale, ts, data = line.strip().split(',', 2)
    info = json.loads(data) # class, code, level, message, flash_version_client, batch_token
    print info['message']
    #print info['class']
    #print info['code']
