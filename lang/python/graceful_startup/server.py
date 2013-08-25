#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
from gevent.server import StreamServer
from gevent.pool import Pool
import os
import time
import socket
import gevent
import umgmt

SLEEP_SEC = 2

# previous server accepted sockets
accepted = set()

def make_server(handler, host='localhost', port=8990):
    pool = Pool(100)
    server = StreamServer((host, port), handler, spawn=pool)

    # graceful startup
    listener_fd, worker_fds = umgmt.graceful_startup(server, 'account', accepted)
    if listener_fd is not None:
        server.set_listener(socket.fromfd(listener_fd, socket.AF_INET, socket.SOCK_STREAM))
    if worker_fds:
        for w in worker_fds:
            s = socket.fromfd(w, socket.AF_INET, socket.SOCK_STREAM)
            gevent.spawn(handler, s, None)

    return server

def handler(sock, addr):
    accepted.add(sock)

    while True:
        sock.sendall(str(accepted) + "\n")
        sock.sendall('hello, lucy, hi\n')
        gevent.sleep(SLEEP_SEC)
        sock.sendall('haha, lucy' + time.ctime() + '\n')
        sock.sendall('bye!\n')

if __name__ == '__main__':
    server = make_server(handler)
    print time.ctime(), 'server started:', server
    server.start()
    server.serve_forever()
