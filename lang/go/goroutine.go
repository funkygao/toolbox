package main

import (
    "fmt"
    "runtime"
)

func sum(a []int, c chan int) {
    sum := 0
    for _, v := range a {
        sum += v
    }

    c <- sum
}

func main() {
    a := []int{7, 2, 8, -9, 4, 0}
    c := make(chan int, 2)
    runtime.GOMAXPROCS(100)
    go sum(a[:len(a)/2], c)
    go sum(a[len(a)/2:], c)
    sum := <- c + <- c
    fmt.Printf("sum=%d\n", sum)
}
