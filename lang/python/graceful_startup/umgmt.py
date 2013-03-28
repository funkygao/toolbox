#encoding=utf-8
'''The micromanagment module provides a tiny server running on a unix domain socket.

It is meant as an alternative to signals for handling graceful server restart.

The underlying unix socket acts as a guard for starting up a server.
Once that socket has be acquired it is assumed that previously bound sockets will be
released and startup can continue.

It does not function in 1 case:
    startup a server instance
    manually remove its sock file
    startup another server instance
'''
import socket
import os
import sys
import errno
import gevent
import passfd
import tempfile

class UmgmtService(object):
    '''The micromanagement acts both as a client and server on unix domain socket.
    '''

    BASE_DIR = tempfile.gettempdir()
    SOCK_SUFFIX = '.sock'
    LAME_DUCK_PERIOD_SECOND = 21

    def __init__(self, server, name):
        self.server = server
        assert hasattr(self.server, 'stop')
        self.name = name

    @property
    def _sockpath(self):
        return os.path.join(self.BASE_DIR, self.name + self.SOCK_SUFFIX)

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
        '''listen_and_serve() -> None | previous server listener socket fd
        '''
        privious_listener = None

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # handshake with possible running server instance
        for i in range(2):
            try:
                s.bind(self._sockpath)
                # if succeed(no server is running on this host), goto _start_accept()
                break
            except socket.error as e:
                if e[0] == errno.EADDRINUSE:
                    c, err = self._dialServer()
                    if err is None:
                        # a server is running on this host
                        os.remove(self._sockpath)
                        privious_listener = self._shutdown_server(c)
                    elif err == errno.ECONNREFUSED or err == errno.ENOTSOCK:
                        # invalid sock file exists
                        os.remove(self._sockpath)
                    else:
                        # unkown error, die early
                        raise Exception(os.strerror(err))
                else:
                    # unkown error
                    raise

        # waiting for next server instance startup handshake
        s.listen(1)
        gevent.spawn(self._start_accept, s)
        return privious_listener

    def _start_accept(self, sock):
        # at this time, self.server.serve_forever() must be called
        # so that self.server.socket is not empty
        c, addr = sock.accept()
        print >>sys.stderr, 'accepted'

        # send listener fd and then close the listener right now
        passfd.sendfd(c, self.server.socket)

        # stop accepting new connections, it will reap it's worker threads
        #self.server.stop() 
        self.server.socket.close()

        print >>sys.stderr, 'waiting for worker to finish after %d seconds...' % self.LAME_DUCK_PERIOD_SECOND
        gevent.sleep(self.LAME_DUCK_PERIOD_SECOND)
        self.server.stop()
        print >>sys.stderr, 'bye!'

    def _shutdown_server(self, sock):
        # get listener fd from previous server instance
        listenerfd, msg = passfd.recvfd(sock)
        return listenerfd

def graceful_startup(server, name):
    return UmgmtService(server, name).listen_and_serve()

