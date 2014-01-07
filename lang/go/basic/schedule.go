package main

import (
    "fmt"
    "time"
)

func schedule(what func(), delay time.Duration) chan bool {
    stop := make(chan bool)

    go func() {
        for {
            what()
            select {
            case <-time.After(delay):
            case <-stop:
                return
            }
        }
    }()

    return stop
}

func main() {
    ping := func() { fmt.Println("#") }

    stop := schedule(ping, 5*time.Millisecond)
    time.Sleep(25 * time.Millisecond)
    stop <- true
    time.Sleep(25 * time.Millisecond)

    fmt.Println("Done")
}
