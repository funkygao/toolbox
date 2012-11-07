package main

import (
    "fmt"
    "math/rand"
    "time"
)

func main() {
    rand.Seed(time.Now().Unix())
    for {
        fmt.Println(rand.Intn(100))
    }
}

