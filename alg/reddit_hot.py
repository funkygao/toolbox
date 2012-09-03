#!/usr/bin/env python
#encoding=utf-8
'''reddit的帖子推荐算法'''
from math import log10, sqrt
from datetime import datetime, timedelta

def epoch_seconds(date):
    td = date - datetime(1970, 1, 1)
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(ups, downs):
    return ups - downs

def hot(ups, downs, post_date):
    """帖子的热度值
    考虑到了如下因素：帖子的新旧，帖子被赞/反对次数"""
    s = score(ups, downs)
    z = max(abs(s), 1) # 帖子的受肯定（否定）的程度
    order = log10(z) # 意味着z=10可以得到1分，z=100可以得到2分
    sign = 1 if s > 0 else -1 if s < 0 else 0 # 表示对文章的总体看法，总体是正面的还是负面的
    seconds = epoch_seconds(post_date) - 1134028003 # 1134028003是reddit公司成立的日期
    return order + sign * seconds / 45000 # 

def confidence(ups, downs):
    """The confidence sort.
       http://www.evanmiller.org/how-not-to-sort-by-average-rating.html"""
    n = ups + downs
    if n == 0:
        return 0

    z = 1.281551565545 # 80% confidence
    p = float(ups) / n

    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z

    return (left - right) / under

if __name__ == '__main__':
    fixtures = [
        (156, 45, datetime(2012, 8, 23)),
        (156, 45, datetime(2012, 8, 24)),
        (1560, 45, datetime(2012, 8, 24)),
        (156000, 45, datetime(2012, 8, 22)),
        (45, 156, datetime(2012, 8, 23)),
    ]
    for (ups, downs, post_date) in fixtures:
        print hot(ups, downs, post_date)

    print '-' * 30

    fixtures = [
        (156, 45),
        (1560, 450),
        (15600, 4500),
    ]
    for (ups, downs) in fixtures:
        print confidence(ups, downs)
