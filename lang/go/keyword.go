/*
codeblock
automatic type inference
_ : blank identifier
`we are`: raw string
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
    _ = iota
    KB = 1 << (10 * iota)
    MB
    GB
    TB
)

const (
    Y = iota
)

func main() {
    var unicodeChar rune = 0x5578
    fmt.Printf("%v %v %v %c\n", MONDAY, X, Y, unicodeChar)
    println(KB, MB, GB)

}
