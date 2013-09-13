#!/usr/bin/env python
#encoding=utf-8

from subprocess import Popen, PIPE
import select
import socket
import sys
import time

HEAD_REPEAT_STEP = 30
SELECT_TIMEOUT = 1
BUFSIZE = 1024

def print_head(domain = '', ips = []):
    if domain:
        print '=' * 5, domain, '=' * 5
    if ips:
        print ips, "\n"
    print '%-16s %-8s %-8s %-10s %-5s %-5s %-5s %-10s %-20s' % (
            'Nginx', 'Now', 'Conn', 'Conn/s', 'Read', 'Write', 'Wait', 'RPS', 'RPSbar')
    print '-'*16, '-------- -------- ---------- ----- ----- ----- ----------', '-' * 20
    sys.stdout.flush()

def get_ips_of_domain(domain):
    r = socket.gethostbyname_ex(domain)
    return r[2]

def handle_nginx_status(stream):
    try:
        print stream.readline(),
    except:
        print 'Nothing to read'

def main():
    domain = sys.argv[1]
    ips = get_ips_of_domain(domain)
    print_head(domain, ips)

    nginx_status_procs = [Popen(['python', 'nginx_status.py', ip, str(ipcolor)], stdout = PIPE, bufsize = BUFSIZE) for ipcolor, ip in enumerate(ips)]
    count = 0
    try:
        while nginx_status_procs:
            for proc in nginx_status_procs:
                retcode = proc.poll()
                if retcode is not None: # proc terminated
                    nginx_status_procs.remove(proc)
                else:
                    if select.select([proc.stdout], [], [], SELECT_TIMEOUT)[0]:
                        handle_nginx_status(proc.stdout)
                        count += 1
                        if count % HEAD_REPEAT_STEP == 0:
                            print_head()
            else:
                time.sleep(1)
                continue
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
