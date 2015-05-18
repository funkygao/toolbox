package main

import (
	"net"
)

func dieIfError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	l, err := net.Listen("tcp", ":1099")
	dieIfError(err)

	for {
		conn, err := l.Accept()
		dieIfError(err)

		go handleConn(conn)
	}
}

func handleConn(conn net.Conn) {
}
