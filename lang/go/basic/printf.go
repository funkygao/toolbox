package main

import "fmt"
import "log"

func main() {
    type X struct {
        x, y int
        z string
    }

    x := X{1, 5, "hello"}
    fmt.Printf("%#v %+v %T %p %x\n", x, x, x, &x, x)
    var b bool
    fmt.Printf("%*s %v %t\n", 10, x.z, b, b) // %t for bool
    var l *log.Logger
    var l1 log.Logger
    fmt.Printf("%#v\n%#v\n", l, l1)

    fmt.Printf("%b\n", 56) // bit
}
