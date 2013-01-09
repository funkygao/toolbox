import phpserialize
from cStringIO import StringIO
    
def decode(data):
    fp = StringIO(data)
    r = {}
    while True:
        npos = data.find('|', fp.tell())
        if npos == -1:
            break
        k = data[fp.tell():npos]
        fp.seek(npos + 1)
        d = phpserialize.load(fp)
        try:
            if sorted(map(int, d.keys())) == range(len(d)):
                d = phpserialize.dict_to_list(d)
        except:
            pass
        r[k] = d
    return r

def encode(vars):
    vars = dict(vars)
    fp = StringIO()
    for k,v in vars.iteritems():
        fp.write(k)
        fp.write('|')
        fp.write(phpserialize.dumps(v))
    return fp.getvalue()

    
if __name__ == '__main__':
    import sys
    t = 'test|s:11:"Hello world";admin|s:8:"username";list|a:3:{i:0;i:7;i:1;i:8;i:2;i:9;}'
    de = decode(t)
    print de
    assert encode(de) == t
    m = 'abc|a:3:{s:1:"a";i:1;s:1:"c";i:3;s:1:"b";i:2;}'
    de = decode(m)
    print de
    assert encode(de) == m

    if len(sys.argv) > 1:
        sess = open(sys.argv[1]).read()
        print decode(sess)
