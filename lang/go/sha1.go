package main

import (
    "fmt"
    "crypto/sha1"
)

func main() {
    s := "we are here"

    h := sha1.New()
    h.Write([] byte(s))

    bs := h.Sum(nil)
    fmt.Println(bs)
    fmt.Printf("%x\n", bs)
}
