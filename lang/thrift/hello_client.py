import sys
sys.path.append('gen-py')

from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from hello import HelloService

sock = TSocket.TSocket('localhost', 8787)
sock.open()
protocol = TBinaryProtocol.TBinaryProtocol(sock)

client = HelloService.Client(protocol)
print '[Client] received:', client.hello_func()
