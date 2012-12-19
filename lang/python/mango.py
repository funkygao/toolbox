#!/usr/bin/env python
#encoding=utf-8

import re
import sys

r = re.compile(r'pkg (?P<pkg>\S+), func (?P<func>\S+).*')
apifile = '/usr/local/go/api/go1.txt'


def main(tag):
    with open(apifile) as f:
        for l in f:
            m = r.match(l)
            if not m:
                continue
            d = m.groupdict()
            pkg, func = d['pkg'], d['func']
            for t in tag:
                tl = t.lower()
                if pkg.lower().find(tl)!=-1 or func.lower().find(tl)!=-1:
                    print pkg, func

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print '''Usage:
        %s keyword, [keyword]''' % sys.argv[0]
        sys.exit(0)

    main(sys.argv[1:])
