package main

import "fmt"

func main() {
    f("Foo")
}

func f(s string) (v int) {
    defer func() {
        fmt.Printf("f(%s) return: %d\n", s, v)
    }()

    return 10
}
