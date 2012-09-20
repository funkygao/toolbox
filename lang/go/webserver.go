package main

import (
    "fmt"
    "net/http"
    "log"
)

func requestHandler(writer http.ResponseWriter, req *http.Request) {
    html := `
<!DOCTYPE html>
<html lang="zh-cn">
<head>
<title>测试一下go作为web server的性能</title>
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
<meta charset="utf-8" />
<body>
<div id="login-bar" class="no-visited">
  <div class="yui3-d3f">
      <ul class="site-login"></ul>
  </div>
</div>
</body>
</html>`
    fmt.Fprintf(writer, html)
}

func main() {
    http.HandleFunc("/", requestHandler)
    err := http.ListenAndServe(":9000", nil)
    if err != nil {
        log.Fatal("ListenAndServe:", err)
    }
}

