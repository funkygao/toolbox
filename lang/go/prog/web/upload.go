package main

import (
    "fmt"
    "io"
    "io/ioutil"
    "net/http"
    "text/template"
)

var uploadTemplate, _ = template.ParseFiles("upload.html")
var errorTemplate, _ = template.ParseFiles("error.html")

func main() {
    if uploadTemplate == nil || errorTemplate == nil {
        panic("template file not exist")
    }

    http.HandleFunc("/", errorHandler(upload))
    http.HandleFunc("/view", errorHandler(view))
    http.ListenAndServe(":8090", nil)
}

func errorHandler(fn http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if e := recover(); e != nil {
                w.WriteHeader(500)
                errorTemplate.Execute(w, e)
            }
        }()
        fn(w, r)
    }
}

func checkError(e error) {
    if e != nil {
        panic(e)
    }
}

func view(w http.ResponseWriter, r *http.Request) {
    fmt.Printf("%#v\n", r)
    w.Header().Set("Content-Type", "image")
    http.ServeFile(w, r, r.FormValue("id"))
}

func upload(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        uploadTemplate.Execute(w, nil)
        return
    }

    f, _, e := r.FormFile("image")
    checkError(e)
    defer f.Close()

    t, e := ioutil.TempFile(".", "image-")
    checkError(e)
    defer t.Close()

    _, e = io.Copy(t, f)
    checkError(e)
    http.Redirect(w, r, "/view?id=" + t.Name(), 302)
}


