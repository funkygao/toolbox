package main

import (
    "fmt"
    "net/rpc"
)

type Args struct {
    A, B int 
}

type Quotient struct {
    Quo, Rem int 
}

func main() {
    client, e := rpc.DialHTTP("tcp", ":1234")
    if e != nil {
        panic(e)
    }

    args := Args{5, 2}
    var reply Quotient

    // sync call
    e = client.Call("Math.Divide", args, &reply)
    if e != nil {
        panic(e)
    }
    fmt.Println(reply)

    // async call
    divCall := client.Go("Math.Divide", args, &reply, nil)
    replyCall := <- divCall.Done
    fmt.Printf("%#v\n", replyCall)
    fmt.Println(replyCall.Reply, replyCall.ServiceMethod)
}
