package main

import (
    "net/http"
    "fmt"
    "os"
    "io"
)

func fetchHtml(url string) {
    resp, err := http.Get(url)
    if err != nil {
        fmt.Println("error occured")
    } else {
        defer resp.Body.Close()

        io.Copy(os.Stdout, resp.Body)
    }
}

func main() {
    const url = "http://www.kaixin001.com"
    const loops = 2250
    
    for i:=0; i<loops; i++ {
        go fetchHtml(url)
    }

    var input string
    fmt.Scanln(&input)
}

