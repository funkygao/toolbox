import json
import sys
import re
import os
import time

os.environ["TZ"]="Asia/Shanghai"
time.tzset()

# grep -h Mongo ~/logs/fp_rstory/history/error_2013110[4-6]* | ./mongo.py  | grep -w -e royal_1  -e roayl_66
for line in sys.stdin:
    locale, ts, data = line.strip().split(',', 2)
    info = json.loads(data) # class, code, level, message, flash_version_client, batch_token
    msg = info['message']
    fts = float(ts)/1000.

    print locale, time.strftime("%d-%T", time.localtime(fts)), msg
