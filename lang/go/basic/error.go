package main

import "errors"
import "fmt"

func main() {
    e := errors.New("shit")
    println(e)
    fmt.Printf("%#v\n", e)

    println(e.Error())
}
