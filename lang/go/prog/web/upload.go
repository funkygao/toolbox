package main

import (
    "io"
    "io/ioutil"
    "net/http"
    "text/template"
)

var uploadTemplate, e = template.ParseFiles("upload.html")


func main() {
    http.HandleFunc("/", upload)
    http.ListenAndServe(":8090", nil)
}

func upload(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        uploadTemplate.Execute(w, nil)
        return
    }

    f, _, e := r.FormFile("image")
    if e != nil {
        http.Error(w, e.Error(), 500)
    }
    defer f.Close()

    t, e := ioutil.TempFile(".", "image-")
    if e != nil {
        http.Error(w, e.Error(), 500)
        return
    }
    defer t.Close()

    if _, e := io.Copy(t, f); e != nil {
        http.Error(w, e.Error(), 500)
        return
    }
    http.Redirect(w, r, "/view?id=" + t.Name(), 302)
}


