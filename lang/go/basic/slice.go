package main

import (
    "fmt"
)

func main() {
    a := [...]int{0, 1, 2, 3, 4, 5}
    s := a[2:4:4]
    s[0] += 100
    s[1] += 200
    fmt.Println(s, a)
    fmt.Println(&a[2], &s[0]) // should be the same addr

    // 超过slice.cap，则重新分配slice底层数组，并copy mem to new addr
    s = append(s, 9)
    fmt.Println(&a[2], &s[0]) // diff addr
}
