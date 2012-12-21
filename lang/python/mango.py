#!/usr/bin/env python
#encoding=utf-8

import re
import sys
import os

r = re.compile(r'pkg (?P<pkg>\S+), (?P<type>\S+) (?P<tag>.+).*')
apifile = '/usr/local/go/api/go1.txt'

def lookup(kws):
    result = set()
    for l in open(apifile):
        m = r.match(l)
        if not m:
            continue
        d = m.groupdict()
        pkg, type, tag = d['pkg'], d['type'], d['tag']
        tag = re.sub(r"\(.*?\)", '', tag) # discard func/method params
        if type == 'method':
            tag = tag.split(' ')[1] #[0] is the receiver
        else:
            tag = tag.split(' ')[0]
        for kw in kws:
            kw = kw.lower()
            if pkg.lower().find(kw)!=-1 or tag.lower().find(kw)!=-1:
                result.add((pkg, tag))

    if len(result) == 1:
        pkg, tag = result.pop()
        os.system('godoc %s %s | less ' % (pkg, tag)) # invoke godoc directly
    else:
        # we have to print the alternatives
        for x in result:
            pkg, tag = x
            print 'godoc', pkg, tag.split(' ')[0], '| less'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print '''Usage:
        %s keyword, [keyword]''' % sys.argv[0]
        sys.exit(0)

    lookup(sys.argv[1:])
