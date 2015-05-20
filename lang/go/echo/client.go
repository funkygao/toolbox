package main

import (
	"flag"
	"log"
	"net"
	"os"
	"strings"
)

var (
	host string
	port string
	c    int
	l    int
)

func init() {
	flag.StringVar(&host, "host", "localhost", "host")
	flag.StringVar(&port, "port", "3333", "port")
	flag.IntVar(&c, "c", 1, "concurrency")
	flag.IntVar(&l, "l", 100, "echo content length")
	flag.Parse()
}

func main() {
	for i := 0; i < c; i++ {
		go doEcho(i)
	}

	select {}
}

func doEcho(seq int) {
	tcpAddr, err := net.ResolveTCPAddr("tcp", host+":"+port)
	if err != nil {
		println("ResolveTCPAddr failed:", err.Error())
		os.Exit(1)
	}

	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		log.Println(err)
		return
	}
	defer conn.Close()

	echoContent := []byte(strings.Repeat("X", l))
	reply := make([]byte, 1024)
	for {
		_, err = conn.Write(echoContent)
		if err != nil {
			log.Println("Write to server failed:", err.Error())
			os.Exit(1)
		}

		_, err = conn.Read(reply)
		if err != nil {
			log.Println("Write to server failed:", err.Error())
			os.Exit(1)
		}

	}

}
