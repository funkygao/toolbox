package main

import (
    "os"
    "fmt"
)

func main() {
    const PASSWD = "/etc/passwd"
    buf := make([]byte, 1024)
    f, err := os.Open(PASSWD)
    if err != nil {
        fmt.Println(err)
    }
    defer f.Close()

    for {
        n, _ := f.Read(buf)
        if n == 0 { // eof
            break
        }
        os.Stdout.Write(buf[:n])
    }
}
