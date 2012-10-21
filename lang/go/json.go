package main

import (
    "fmt"
    json "encoding/gob"
    "log"
    "os"
)

type Address struct {
    Type, city, country string
}

type Vcard struct {
    FirstName, LastName string
    Adresses []*Address
    Remark string
}

func main() {
    const JSON_FILE = "vc.json"

    pa := &Address{"private", "beijing", "China"}
    wa := &Address{"work", "shanghai", "China"}
    vc := Vcard{"funky", "gao", []*Address{pa, wa}, "none"}

    file, _  := os.OpenFile(JSON_FILE, os.O_CREATE|os.O_WRONLY, 0600)

    enc := json.NewEncoder(file)
    if err := enc.Encode(vc); err != nil {
        log.Fatal(err)
    }
    //file.Close()

    f, _ := os.Open(JSON_FILE)
    dec := json.NewDecoder(f)
    x := new(Vcard)
    fmt.Printf("%v %#v\n", dec.Decode(x), x)

}
