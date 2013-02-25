package main

import (
    "fmt"
    "testing"
    "os"
    "net/rpc"
    "runtime/pprof"
)

type Args struct {
    A, B int 
}

type Quotient struct {
    Quo, Rem int 
}

var client *rpc.Client
var e error

func callRpc() {
    if client == nil {
    client, e = rpc.DialHTTP("tcp", ":1234")
    if e != nil {
        panic(e)
    }
}

    args := Args{5, 2}
    var reply Quotient

    // sync call
    e = client.Call("Math.Divide", args, &reply)
    if e != nil {
        panic(e)
    }
}

func main() {
    f, e := os.Create("a.prof")
    if e != nil {
        panic(e)
    }

    e = pprof.StartCPUProfile(f)
    if e != nil {
        panic(e)
    }

    defer pprof.StopCPUProfile()
    //r := testing.Benchmark(benchmarkRpcCallDivide)
    //fmt.Println(r.T)
    fmt.Printf("%s\n", testing.Benchmark(benchmarkRpcCallDivide).String())
}

func benchmarkRpcCallDivide(b *testing.B) {
    for i:=0; i<b.N; i++ {
        callRpc()
    }
}
