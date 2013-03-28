#!/usr/bin/env python
from gevent.server import StreamServer
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import os
import time
import socket
import gevent
import umgmt

def make_server(handler, host='localhost', port=8990):
    pool = Pool(100)
    server = StreamServer((host, port), handler, spawn=pool)

    # graceful startup
    listenerfd = umgmt.graceful_startup(server, 'account')
    if listenerfd is not None:
        server.set_listener(socket.fromfd(listenerfd, socket.AF_INET, socket.SOCK_STREAM))

    return server

def handler(sock, addr):
    print sock, addr, time.ctime()
    sock.sendall('hello, lucy, bye\n')
    sock.sendall(str(addr) + "\n")
    gevent.sleep(1)
    sock.close()

if __name__ == '__main__':
    server = make_server(handler)
    print 'server started:', server, 'at', time.ctime()
    server.start()
    server.serve_forever()
