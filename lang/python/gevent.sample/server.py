#!/usr/bin/env python
from gevent.server import StreamServer
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import os
import socket
import gevent
import umgt

def should_grace_shutdown(s):
    u = umgt.Umgmt(s)
    u.ListenAndServe('_.sock')

def make_server(handler, host='localhost', port=8990):
    pool = Pool(100)
    server = StreamServer((host, port), handler, spawn=pool)
    should_grace_shutdown(server)
    #gevent.sleep(1)
    return server

def handler(sock, addr):
    print sock, addr
    #gevent.sleep(1)
    sock.sendall('hello, lucy\n')

if __name__ == '__main__':
    server = make_server(handler)
    print server
    server.serve_forever()
