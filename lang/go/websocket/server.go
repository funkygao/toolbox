package main

import (
    "code.google.com/p/go.net/websocket"
    "fmt"
    "net/http"
    "log"
)

func main() {
    http.Handle("/", websocket.Handler(handler))
    log.Println("listen on :4000")
    http.ListenAndServe("localhost:4000", nil)
}

func handler(ws *websocket.Conn) {
    var s string
    fmt.Fscan(ws, &s)
    log.Println("Received:", s)
    fmt.Fprint(ws, "How are you")
}
