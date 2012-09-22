package main

type FileHandle interface {
    Open()
    Close()
}

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

func main() {
    x := new(GaoFile)
    d(*x)

    var y = GaoFile{}
    d(y)
}


