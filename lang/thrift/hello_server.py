import sys
sys.path.append("gen-py")
sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages")

from thrift.transport import TSocket 
from thrift.server import TServer 
from hello import HelloService

class HelloHandler:
    def hello_func(self):
        print '[Server] handling client request'
        return 'hello thrift, from py server'


handler = HelloHandler()
processor = HelloService.Processor(handler)
listen_sock = TSocket.TServerSocket(port=8787)
server = TServer.TSimpleServer(processor, listen_sock)

print '[Server] started'
server.serve()

