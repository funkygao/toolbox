package main

import (
    "bufio"
    "os"
    "fmt"
    "net"
    "time"
)

func check(err error) {
    if err != nil {
        panic(err)
    }
}

func main() {
    maddr, err := net.ResolveUDPAddr("udp", "239.255.43.99:1090")
    check(err)
    fmt.Printf("%#v\n", maddr)
    conn, err := net.ListenMulticastUDP("udp", nil, maddr)
    check(err)
    go func(conn *net.UDPConn) {
        for {
            buf := make([]byte, 12)
            now := time.Now()
            conn.SetDeadline(now.Add(time.Second * 5))
            n, addr, err :=conn.ReadFromUDP(buf)
            fmt.Println("\ninput from udp:", buf, n, addr, err)
        }
    }(conn)

    reader := bufio.NewReader(os.Stdin)
    for {
        fmt.Print("Input: ")
        t, _, _ := reader.ReadLine()
        if len(t) == 0 {
            fmt.Println("Bye")
            os.Exit(0)
        }
        fmt.Println("Got input:", t)
        b := make([]byte, 12)
        copy(b, t)
        n, err := conn.WriteToUDP(b, maddr)
        check(err)
        fmt.Println("Sent to udp:", n, err)
    }

}
