package main

import (
    "fmt"
    "strings"
    "reflect"
)

type MyStruct struct {
    name string
}

func (this *MyStruct)GetName() string {
    return this.name
}

func main() {
    s := "we are here"
    fmt.Println(reflect.TypeOf(s))
    fmt.Printf("%#v\n", reflect.TypeOf(s))
    fmt.Println(reflect.ValueOf(s))

    println(strings.Repeat("-", 50))
    a := new(MyStruct)
    a.name = "funky gao"
    t := reflect.TypeOf(a)
    fmt.Println(t)
    fmt.Println(t.NumMethod())
    b := reflect.ValueOf(a).MethodByName("GetName").Call([] reflect.Value{})
    fmt.Println(b[0])
}

