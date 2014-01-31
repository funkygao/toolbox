import sys
sys.path.append('gen-py')
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')

from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from hello import HelloService

sock = TSocket.TSocket('localhost', 8787)
sock.open()
protocol = TBinaryProtocol.TBinaryProtocol(sock)

client = HelloService.Client(protocol)
print '[Client] received:', client.hello_func()
