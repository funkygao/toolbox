#!/usr/bin/env python
from gevent.server import StreamServer

def handle(socket, addr):
    print socket, addr
    socket.send('hello in telnet\n')
    for i in range(5):
        socket.send(str(i) + '\n')

    socket.close()

def start_server(host='localhost', port=8888):
    server = StreamServer((host, int(port)), handle)
    print 'server at localhost:8888'
    server.serve_forever()

if __name__ == '__main__':
    start_server()
