package main

import (
    "fmt"
    "testing"
    "net/rpc"
)

type Args struct {
    A, B int 
}

type Quotient struct {
    Quo, Rem int 
}

func callRpc() {
    client, e := rpc.DialHTTP("tcp", ":1234")
    if e != nil {
        panic(e)
    }
    defer client.Close()

    args := Args{5, 2}
    var reply Quotient

    // sync call
    e = client.Call("Math.Divide", args, &reply)
    if e != nil {
        panic(e)
    }
}

func main() {
    r := testing.Benchmark(benchmarkRpcCallDivide)
    fmt.Println(r.T)
    fmt.Printf("%s\n", testing.Benchmark(benchmarkRpcCallDivide).String())
}

func benchmarkRpcCallDivide(b *testing.B) {
    for i:=0; i<b.N; i++ {
        callRpc()
    }
}
