package main

import (
    "time"
)

func main() {
    var c chan bool = make(chan bool)
    c1 := make(chan int)

    go func() {
        time.Sleep(1e9) // time.Sleep(time.Second * 1)
        c <- true
    }()

    select {
    case x := <- c1:
        println("omg", x)
    case <- c:
        println("timeout")
    }
}
