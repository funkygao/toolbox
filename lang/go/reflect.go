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

func Allocate(i interface{}, limit ...int) (n interface{}) {
    switch v := reflect.ValueOf(i); v.Kind() {
    case reflect.Slice:
        l := v.Cap()
        if len(limit) > 0 {
            l = limit[0]
        }
        n = reflect.MakeSlice(v.Type(), l, l).Interface()
    case reflect.Map:
        n = reflect.MakeMap(v.Type())
    }
    return
}

func Duplicate(i interface{}) (clone interface{}) {
    if clone = Allocate(i); clone != nil {
        switch clone:= reflect.ValueOf(clone); clone.Kind() {
        case reflect.Slice:
            reflect.Copy(clone, reflect.ValueOf(i))
        case reflect.Map:
            m := reflect.ValueOf(i)
            for _, k := range m.MapKeys() {
                clone.SetMapIndex(k, m.MapIndex(k))
            }
        }
    }
    return
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

    x := []string{"a", "b"}
    n := Duplicate(x)
    fmt.Printf("%#v\n", n)
}

