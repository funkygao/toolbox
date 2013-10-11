#!/usr/bin/env python
'''dlog error_* analyzer'''

import json
import sys
import re

digitRegex = re.compile(r'\d+')

for line in sys.stdin:
    locale, ts, data = line.strip().split(',', 2)
    info = json.loads(data) # class, code, level, message, flash_version_client, batch_token
    msg = info['message']
    print digitRegex.sub('?', msg)
    #print info['class']
    #print info['code']
