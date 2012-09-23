// client server with goroutine
package main

type Request struct {
    a, b int
    replyCh chan int  // replay channel inside the request
}

type binOp func(a, b int) int

func handleRequest(op binOp, req *Request) {
    req.replyCh <- op(req.a, req.b)
}

func server(op binOp, service chan *Request) {
    for {
        req := <- service  // request arrives here

        go handleRequest(op, req)
    }
}

func startServer(op binOp) chan * Request {
    reqCh := make(chan *Request)
    go server(op, reqCh)
    return reqCh
}

func main() {
    op := func(a, b int) int {
        return a + b
    }
    addr := startServer(op)

    // build the requests
    const N = 100
    var reqs [N]Request
    for i:=0; i<N; i++ {
        req := &reqs[i]
        req.a, req.b = i, N
        req.replyCh = make(chan int)
        addr <- req
    }

    // get result
    for i:=N-1; i>=0; i-- { // doesn't matter what order
        println("Got:", <- reqs[i].replyCh)
    }
}

