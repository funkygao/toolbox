package main

import "fmt"

func main() {
    type X struct {
        x, y int
        z string
    }

    x := X{1, 5, "hello"}
    fmt.Printf("%#v %+v %T\n", x, x, x)
    fmt.Printf("%*s\n", 10, x.z)
}
