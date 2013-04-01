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
import time
import errno
import gevent
import passfd
import tempfile

class UmgmtService(object):
    '''The micromanagement acts both as a client and server on unix domain socket.
    '''

    BASE_DIR = tempfile.gettempdir()
    SOCK_SUFFIX = '.sock'
    WORKER_NUM_SUFFIX = '.num'
    LAME_DUCK_PERIOD_SECOND = 1

    def __init__(self, server, name, accepted):
        assert hasattr(server, 'stop')
        self.server = server
        self.name = name
        self.accepted = accepted

    @property
    def _workernpath(self):
        '''IPC through this temp file

        Parent tells how many accepted sockets exist through this temp file.
        '''
        return os.path.join(self.BASE_DIR, self.name + self.WORKER_NUM_SUFFIX)

    @property
    def _sockpath(self):
        '''Unix domain socket file'''
        return os.path.join(self.BASE_DIR, self.name + self.SOCK_SUFFIX)

    def _dial_server(self):
        '''_dial_server() -> sock, errno

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
        privious_listener, accepted_socks = None, None

        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # handshake with possible running server instance
        for i in range(2):
            try:
                s.bind(self._sockpath)
                # if succeed(no server is running on this host), goto _start_accepting()
                break
            except socket.error as e:
                if e[0] == errno.EADDRINUSE:
                    c, err = self._dial_server()
                    if err is None:
                        # a server is running on this host
                        os.remove(self._sockpath)
                        privious_listener, accepted_socks = self._shutdown_server(c)
                    elif err == errno.ECONNREFUSED or err == errno.ENOTSOCK:
                        # invalid sock file exists
                        os.remove(self._sockpath)
                    else:
                        # unkown error, die early
                        raise Exception(os.strerror(err))
                else:
                    # unkown error
                    raise

        # waiting for new server instance startup handshake
        s.listen(1)
        gevent.spawn(self._start_accepting, s)
        return privious_listener, accepted_socks

    def _notify_worker_fds_num(self, n):
        with open(self._workernpath, 'w') as f:
            f.write(str(n))

    def _get_worker_fds_num(self):
        return int(open(self._workernpath, 'r').read())

    def _start_accepting(self, sock):
        '''
                    server1                 server2
                       |                dial   |
                       |<----------------------|
                       | accept                |
                       |                       |
                       | listener fd           |
                       |---------------------->|
                       |                       |
                       | num of worker fds     |
                       |---------------------->|
                       |                       |
                       | worker fd 1by1        |
                       |---------------------->|
                       |                       |
        '''
        # at this time, self.server.serve_forever() must be called
        # so that self.server.socket is not empty
        c, addr = sock.accept()
        print >>sys.stderr, time.ctime(), 'accepted from', c

        os.unlink(self._workernpath)

        # send listener fd and then close the listener right now
        print >>sys.stderr, time.ctime(), 'sending listener', self.server.socket
        passfd.sendfd(c, self.server.socket)

        # close my listener, so that my accepted workers will be snapshotted
        self.server.socket.close() 

        self._notify_worker_fds_num(len(self.accepted))

        # pass fd of worker one by one
        for s in self.accepted:
            print >>sys.stderr, time.ctime(), 'sending client fd', s
            passfd.sendfd(c, s)

        print >>sys.stderr, time.ctime(), 'waiting for worker to finish after %d seconds...' % self.LAME_DUCK_PERIOD_SECOND
        gevent.sleep(self.LAME_DUCK_PERIOD_SECOND)
        self.server.stop()
        print >>sys.stderr, time.ctime(), 'bye!'

    def _shutdown_server(self, sock):
        '''
        TODO divide this into 2 parts:
            1. pass listener socket
            2. pass accepted sockets
        '''
        # get listener fd from previous server instance
        listenerfd, msg = passfd.recvfd(sock)
        print >>sys.stderr, time.ctime(), 'got listener', listenerfd

        accepted = set()
        for _ in range(self._get_worker_fds_num()):
            a, msg = passfd.recvfd(sock)
            print >>sys.stderr, time.ctime(), 'recved accepted', a
            accepted.add(a)
        return listenerfd, accepted

def graceful_startup(server, name, accepted):
    return UmgmtService(server, name, accepted).listen_and_serve()

