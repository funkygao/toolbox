#!/usr/bin/env python
import gevent
from gevent import socket

urls = ['www.google.com', 'www.example.com', 'www.python.org']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=2)
for job in jobs:
    print job.value, job
