import socket
import os
import sys
import errno
import gevent

class Umgmt(object):
    def __init__(self, server):
        self.server = server

    def _dial(self, sockpath):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(sockpath)
        except socket.error as e:
            return None, e[0]
        return s, None

    def ListenAndServe(self, sockpath):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock = s
        for i in range(2):
            print i, sockpath + ' exists:', os.path.exists(sockpath)
            try:
                s.bind(sockpath)
                print 'bind ok'
                break
            except socket.error as e:
                print 'bind failed'
                if e[0] == errno.EADDRINUSE:
                    c, err = self._dial(sockpath)
                    if err is None:
                        self.shutdown(c)
                        os.remove(sockpath)
                    elif err == errno.ECONNREFUSED:
                        os.remove(sockpath)
                        print 'remove', sockpath
                    else:
                        print 'bingo'
                else:
                    print e, 'shit'
                    sys.exit(1)

        gevent.spawn(self.listen_loop, s)

    def listen_loop(self, s):            
        # just got one request ok
        s.listen(1)
        conn, addr = s.accept()
        data = conn.recv(1024)
        print 'got', data
        self.server.stop()
        gevent.sleep(1)
        print 'bye, old'
        sys.exit(0)

    def shutdown(self, sock):
        sock.sendall('blah')
        print 'blah sent'



