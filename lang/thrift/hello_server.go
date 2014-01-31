package main

import (
	"./gen-go/hello"
	"fmt"
	"git.apache.org/thrift.git/lib/go/thrift"
)

type HelloServiceImpl struct {
}

func (this *HelloServiceImpl) HelloFunc() (r string, err error) {
	fmt.Println("[Server] got request")
	return "Hello from go server", nil
}

func main() {
	transportFactory := thrift.NewTFramedTransportFactory(thrift.NewTTransportFactory())
	protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()
	serverTransport, err := thrift.NewTServerSocket(":8787")
	if err != nil {
		panic(err)
	}

	handler := &HelloServiceImpl{}
	processor := hello.NewHelloServiceProcessor(handler)

	server := thrift.NewTSimpleServer4(processor, serverTransport, transportFactory, protocolFactory)
	fmt.Println("Server ready")
	if err := server.Serve(); err != nil {
		panic(err)
	}
}
