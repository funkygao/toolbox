package main

import (
    "fmt"
    "time"
)

func main() {
    timer1 := time.NewTimer(time.Second * 2)

    <- timer1.C
    fmt.Println("timer1 expired")

    
    timer2 := time.NewTimer(time.Second * 2)
    go func() {
        <- timer2.C
        println("t2 expired")
    }()
    if timer2.Stop() {
        println("t2 stopped")
    }

}

