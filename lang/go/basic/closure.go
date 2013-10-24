package main

func Adder() func(int) int {
    var x int
    return func(v int) int {
        x += v
        return x
    }
}

func main() {
    a := Adder()
    println(a(1))
    println(a(20)) // will print 21 instead of 20: closure
}
