/*
    goroutine1  goroutine2  goroutine3  goroutineN
        |           |           |           |
         -----------------------------------
                        |
                        | multiplex
                        |
          goroutine-scheduler(runtime pkg)
                        |
             GOMAXPROCS | thread pool
                        |
                 -----------
                |           |
            os thread   os thread
            ---------   ---------
*/
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

    runtime.Goexit()  // unecessary
}

func main() {
    cpus := runtime.NumCPU()
    fmt.Println("num of cpu:", cpus)

    runtime.GOMAXPROCS(cpus)

    a := []int{7, 2, 8, -9, 4, 0}
    c := make(chan int, 2)
    runtime.GOMAXPROCS(100)
    go sum(a[:len(a)/2], c)
    go sum(a[len(a)/2:], c)
    sum := <- c + <- c
    fmt.Printf("sum=%d\n", sum)
}
