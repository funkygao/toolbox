package main

import (
	"./gen-go/hello"
	"fmt"
	"git.apache.org/thrift.git/lib/go/thrift"
	"time"
)

func main() {
	t1 := time.Now()
	transportFactory := thrift.NewTFramedTransportFactory(thrift.NewTTransportFactory())
	protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()

	transport, err := thrift.NewTSocket(":8787")
	if err != nil {
		panic(err)
	}

	useTransport := transportFactory.GetTransport(transport)
	client := hello.NewHelloServiceClientFactory(useTransport, protocolFactory)
	if err := transport.Open(); err != nil {
		panic(err)
	}
	defer transport.Close()

	for i := 0; i < 1000; i++ {
		r, _ := client.HelloFunc()
		fmt.Println(r, time.Since(t1))
		t1 = time.Now()
	}

}
