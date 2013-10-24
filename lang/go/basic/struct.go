package main

import (
    "unsafe"
    "github.com/kr/pretty"
)

type T struct {
    a, b int
    s string "haha" // field tag, only reflect can access it
    f func(int, int) string // func field
    _ bool // never used
}

func main() {
    var t *T = new(T)
    var t1 T
    pretty.Printf("%v, %v, %d %d", *t, t1, unsafe.Sizeof(t), unsafe.Sizeof(t1))
}
