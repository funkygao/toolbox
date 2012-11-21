package main

import (
    "errors"
    "fmt"
    "net"
    "net/rpc"
    "net/http"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

type Math int

func (this *Math) Divide(args *Args, reply *Quotient) error {
    if args.B == 0 {
        return errors.New("divide by zero")
    }

    reply.Quo = args.A / args.B
    reply.Rem = args.A % args.B
    return nil
}

func main() {
    m := new(Math)
    rpc.Register(m)
    rpc.HandleHTTP()
    l, e := net.Listen("tcp", ":1234")
    if e != nil {
        panic(e)
    }

    fmt.Println("start to serve")
    http.Serve(l, nil)
}
