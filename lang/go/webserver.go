package main

import (
    "fmt"
    "net/http"
    "runtime"
)

func requestHandler(writer http.ResponseWriter, req *http.Request) {
    html := ` <!DOCTYPE html> <html lang="zh-cn"> <head> <title>测试一下go作为web server的性能</title> <meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" /> <meta charset="utf-8" /> <body> <div id="login-bar" class="no-visited"> <div class="yui3-d3f"> <ul class="site-login"></ul> </div> </div> </body> </html>`
    fmt.Fprintf(writer, html)
}

func main() {
    runtime.GOMAXPROCS(100)  // 并发协程数
    http.HandleFunc("/", requestHandler)
    http.ListenAndServe(":9000", nil)
}

