package main

// #include <math.h>
// #cgo LDFLAGS: -lm
// #cgo CFLAGS: -Dfunky -I/usr/include
import "C"

func pow(b, e float64) float64 {
    return float64(C.pow(C.double(b), C.double(e)))
}

func main() {
    println(pow(3, 2))
}
