// lzop -dcf /kx/dlog/121012/lz.121012-11* | ./amf
package main

import (
    "bufio"
    "flag"
    "fmt"
    "io"
    "log"
    "os"
    "runtime"
    "strconv"
    "strings"
    "sync"
)

const (
    LINE_CH_BUFFER = 10
    DEFAULT_IN_READER = "stdin"
)

var lock *sync.Mutex

var eof chan bool = make(chan bool)   // all the specified dlog lines are read
var exit chan bool = make(chan bool)  // let main goroutine exit

// a single line meta info
type Request struct {
    // TODO http_method is useless?
    http_method, uri, rid, class, method, args string
    time int16
}

// line validator for Request
func (req Request) ValidateLine(line string) bool {
    var items = []string{"AMF_SLOW", "100.123", "PHP.CDlog"}
    for _, item := range items {
        if !strings.Contains(line, item) {
            return false
        }
    }

    return false
}

// parse a line into meta info
// ret -> valid line?
func (req *Request) ParseLine(line string) bool {
    if !req.ValidateLine(line) {
        return false
    }

    // major parts seperated by space
    parts := strings.Split(line, " ")

    // uri related
    uriInfo := strings.Split(parts[5], "+")
    if len(uriInfo) < 3 {
        log.Fatal(line)
    }
    req.http_method, req.uri, req.rid = uriInfo[0], uriInfo[1], uriInfo[2]

    // class call and args related
    callRaw := strings.Replace(parts[6], "{", "", -1) 
    callRaw = strings.Replace(callRaw, "}", "", -1) 
    callRaw = strings.Replace(callRaw, "\"", "", -1) 
    callRaw = strings.Replace(callRaw, "[", "", -1) 
    callRaw = strings.Replace(callRaw, "]", "", -1) 
    callRaw = strings.Replace(callRaw, ",", ":", -1) 
    callInfo := strings.Split(callRaw, ":")
    time, err := strconv.Atoi(callInfo[1])
    if err != nil {
        log.Fatal(line, err)
    }
    req.time = int16(time)
    req.class = callInfo[3]
    if len(callInfo) > 10 {
        req.method = callInfo[10]
    }

    return true // valid
}

// better printable Request
func (req *Request) String() string {
    return fmt.Sprintf("{http:%s uri:%s rid:%s class:%s method:%s time:%d args:%s}",
        req.http_method, req.uri, req.rid, req.class, req.method, req.time, req.args)
}

// read lines from stdin
func readLines(file *os.File) {
    inputReader := bufio.NewReader(file)
    chLine := make(chan string, LINE_CH_BUFFER)
    for {
        line, err := inputReader.ReadString('\n')
        if err != nil {
            if err != io.EOF {
                log.Fatal(err)
            }
            eof <- true
            break
        }

        chLine <- line
        go handleLine(chLine)
    }
}

// raw line handler
func handleLine(chLine chan string) {
    var line string = <- chLine

    req := new(Request)
    if !req.ParseLine(line) {
        return
    }

    fmt.Printf("%5d%36s%20s %s\n", req.time, req.uri, req.class, req.method)
}

func renderReportHeader() {
    println(strings.Repeat("=", 100))
    println(strings.Repeat(" ", 10), "Final Report")
    println(strings.Repeat("=", 100))
}

func renderReport() {
    <- eof
    renderReportHeader()
    exit <- true
}

func main() {
    // parallel level
    runtime.GOMAXPROCS(runtime.NumCPU() + 1)

    // cli options
    logFile := flag.String("f", DEFAULT_IN_READER, "specify dlog file[s] path, wildcard permitted")
    flag.Parse()

    // init done! start the job
    if *logFile == DEFAULT_IN_READER {
        go readLines(os.Stdin)
    }

    go renderReport()

    <- exit
}

