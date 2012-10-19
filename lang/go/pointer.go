package main

import (
    "fmt"
)

func main() {
    s := "hello"
    var p *string
    p = &s
    *p = "booo" // s content will change accordingly
    fmt.Println(s)
}
