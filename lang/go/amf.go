// lzop -dcf /kx/dlog/121012/lz.121012-11* | grep AMF_SLOW | grep "100\.123" | grep "KP:PHP\.CDlog" | amf
package main

import (
    "fmt"
    "bufio"
    "log"
    "os"
    "runtime"
    "strings"
    "strconv"
)

type Request struct {
    http_method, uri, rid, class, method, args string
    time int 
}

func (req *Request) parse(line string) {
    var err error
    parts := strings.Split(line, " ")

    uriInfo := strings.Split(parts[5], "+")
    req.http_method, req.uri, req.rid = uriInfo[0], uriInfo[1], uriInfo[2]

    callRaw := strings.Replace(parts[6], "{", "", -1) 
    callRaw = strings.Replace(callRaw, "}", "", -1) 
    callRaw = strings.Replace(callRaw, "\"", "", -1) 
    callRaw = strings.Replace(callRaw, "[", "", -1) 
    callRaw = strings.Replace(callRaw, "]", "", -1) 
    callRaw = strings.Replace(callRaw, ",", ":", -1) 
    callInfo := strings.Split(callRaw, ":")
    req.time, err = strconv.Atoi(callInfo[1])
    if err != nil {
        log.Fatal(err)
    }
    req.class = callInfo[3]
    if len(callInfo) > 10 {
        req.method = callInfo[10]
    }
}

func (req *Request) String() string {
    return fmt.Sprintf("{http:%s uri:%s rid:%s class:%s method:%s time:%d args:%s}",
    req.http_method, req.uri, req.rid, req.class, req.method, req.time, req.args)
}

func readLines() {
    inputReader := bufio.NewReader(os.Stdin)
    lineCh := make(chan string, 10)
    for {
        line, err := inputReader.ReadString('\n')
        if err != nil {
            // EOF
            fmt.Println(err)
            break
        }

        lineCh <- line
        go handleLine(lineCh)
    }
}

func handleLine(lineCh chan string) {
    var line string = <- lineCh

    req := new(Request)
    req.parse(line)
    fmt.Printf("%5d%36s%20s %s\n", req.time, req.uri, req.class, req.method)
}

func main() {
    runtime.GOMAXPROCS(runtime.NumCPU() + 1)

    readLines()
}
