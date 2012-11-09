package main

// #include <math.h>
// #include <stdio.h>
// #include <stdlib.h>
// #cgo LDFLAGS: -lm
// #cgo CFLAGS: -Dfunky -I/usr/include
import "C"
import "unsafe"

type File C.FILE

func Open(path, mode string) *File {
    cpath, cmode := C.CString(path), C.CString(mode)
    defer C.free(unsafe.Pointer(cpath))
    defer C.free(unsafe.Pointer(cmode))

    return (*File)(C.fopen(cpath, cmode))
}

func (this *File) Get(n int) string {
    cbuf := make([]C.char, n)
    return C.GoString(C.fgets(&cbuf[0], C.int(n), (*C.FILE)(this)))
}

func pow(b, e float64) float64 {
    return float64(C.pow(C.double(b), C.double(e)))
}

func main() {
    println(pow(3, 2))
}
