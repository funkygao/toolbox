#!/usr/bin/env python
# normalize sql statement

import re

def normalize_sql(sql):
    sql = re.sub(r"'(.*?)'", 'S', sql)
    return re.sub(r"\d{1,}", 'N', sql)

if __name__ == '__main__':
    sql = "insert into s_user_gamestory_request (appid, num, uid, memo) values(1226, 3, 141571846, 'demo only')"
    print sql
    print normalize_sql(sql)
