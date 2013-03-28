#encoding=utf-8
'''The micromanagment module provides a tiny server running on a unix domain socket.

It is meant as an alternative to signals for handling graceful server restart.

The underlying unix socket acts as a guard for starting up a server.
Once that socket has be acquired it is assumed that previously bound sockets will be
released and startup can continue. 
'''
import socket
import os
import sys
import errno
import gevent
import passfd

class UmgmtService(object):
    '''The micromanagement acts both as a client and server.
    '''

    BASE_DIR = '/tmp/'
    CMD_SHUTDOWN = 'shutdown'

    def __init__(self, server, name):
        self.server = server
        self.name = name

    @property
    def _sockpath(self):
        return self.BASE_DIR + self.name + '.sock'

    def _dialServer(self):
        '''_dial() -> sock, errno

        client connect to server on unix domain socket.
        '''
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(self._sockpath)
        except socket.error as e:
            return None, e[0]
        return s, None

    def listen_and_serve(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # handshake with possible running server instance
        for i in range(2):
            try:
                s.bind(self._sockpath)
                # if succeed(no server is running on this host), goto _listen_loop
                break
            except socket.error as e:
                if e[0] == errno.EADDRINUSE:
                    c, err = self._dialServer()
                    if err is None:
                        # a server is running on this host
                        os.remove(self._sockpath)
                        self._shutdownServer(c)
                    elif err == errno.ECONNREFUSED or err == errno.ENOTSOCK:
                        # sock exists, but server was lost or invalid sock file
                        # and then, try bind() again
                        os.remove(sockpath)
                    else:
                        # unkown error, die early
                        raise Exception(os.strerror(err))
                else:
                    # unkown error
                    raise

        # waiting for next server instance startup handshake
        gevent.spawn(self._listen_loop, s)

    def _listen_loop(self, sock):            
        # just got one request ok
        sock.listen(1)
        c, addr = sock.accept()
        data = c.recv(1024)
        # send listener fd and then close the listener right now
        self.server.stop()
        gevent.sleep(2)
        sys.exit(0)

    def _shutdownServer(self, sock):
        sock.sendall(self.CMD_SHUTDOWN)
        #self.server.set_listener(passed_sockfd)

def graceful_startup(server, name):
    us = UmgmtService(server, name)
    us.listen_and_serve()

