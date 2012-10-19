package main

import "fmt"

func main() {
    type X struct {
        x, y int
        z string
    }

    x := X{1, 5, "hello"}
    fmt.Printf("%#v %+v %T\n", x, x, x)
    var b bool
    fmt.Printf("%*s %v\n", 10, x.z, b)
}
