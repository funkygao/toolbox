package main

import (
        "flag"
        "github.com/kr/beanstalk"
        "log"
        "time"
)

// Get Parameters from cli
var workers = flag.Int("c", 1, "number of concurrent workers, default to 1")
var count = flag.Int("n", 10000, "Counts of push operation in each worker, default to 10000")
var host = flag.String("h", "localhost:11300", "Host to beanstalkd, default to localhost:11300")
var size = flag.Int("s", 256, "Size of data, default to 256. in byte")

func testWorker(h string, count int, size int, ch chan int) {
        conn, e := beanstalk.Dial("tcp", h)
        defer conn.Close()
        data := make([]byte, size)
        if e != nil {
                log.Fatal(e)
        }
        for i := 0; i < count; i++ {
                _, err := conn.Put(data, 0, 0, 120*time.Second)
                if err != nil {
                        log.Fatal(err)
                }
        }
        ch <- 1
}

func main() {
        flag.Parse()
        log.Println("Starting worker: ", *workers)
        log.Println("Count of each worker: ", *count)
        log.Println("Target host: ", *host)
        log.Println("Benchmarking, be patient ...")
        ch := make(chan int)
        t0 := time.Now()

        // Fork goroutine
        for i := 0; i < *workers; i++ {
                go testWorker(*host, *count, *size, ch)
        }

        // Wait for return
        for i := 0; i < *workers; i++ {
                <-ch
        }

        delta := time.Now().Sub(t0)
        log.Println("---------------")
        log.Println("Elapsed Time: ", delta)
        log.Println("Result: ", float64(*workers)*float64(*count)/delta.Seconds(), " req/s")
}
