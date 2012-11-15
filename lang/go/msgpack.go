package main

import (
    "github.com/msgpack/msgpack-go"
    "fmt"
    "bytes"
)

func main() {
    buf := new(bytes.Buffer)
    n, e := msgpack.Pack(buf, 12343434)
    fmt.Println(n, e)
    fmt.Printf("%#v\n", buf)

    value, n, e := msgpack.Unpack(buf)
    fmt.Printf("%#v, %#v\n", e, value)
    fmt.Println(n, value.Interface())
}
