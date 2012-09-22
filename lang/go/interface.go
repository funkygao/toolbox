package main

import "fmt"

type FileHandle interface {
    Open()
    Close()
}

type Any interface {}

type GaoFile struct {
}

func (f GaoFile)Open() {
    println("open")
}

func (f GaoFile)Close() {
    println("close")
}

func d(f FileHandle) {
    f.Open()
    f.Close()
}

func demoAny() {
    var x Any
    x = 5
    x = 34.5
    println("any", x)
    fmt.Printf("%#v\n", x)
}

func main() {
    x := new(GaoFile)
    d(*x)

    var y = GaoFile{}
    d(y)

    demoAny()
}

