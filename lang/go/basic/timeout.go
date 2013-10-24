package main

import "time"

func main() {
    ch := make(chan int)
    go func() {
        time.Sleep(time.Second * 2)
        ch <- 1
    }()

    select {
    case r := <- ch:
        println("ok", r)
    case <- time.After(time.Second * 3):
        println("timeout")
        break
    }
}
