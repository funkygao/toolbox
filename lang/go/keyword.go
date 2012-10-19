/*
_ : blank identifier
anonymous 
type I int8: underlying type
*/
package main

import (
    "fmt"
)

const (
    SUNDAY = iota + 1 // 1
    MONDAY // 2
    TUESDAY // 3

    X = iota // 3
)

const (
    Y = iota
)

func main() {
    fmt.Printf("%v %v %v\n", MONDAY, X, Y)
}
