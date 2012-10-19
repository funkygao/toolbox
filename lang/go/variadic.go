package main

func min(x ...int) int {
    if len(x) == 0 {
        return 0
    }

    m := x[0]
    for _, v := range(x) {
        if v < m {
            m = v
        }
    }
    return m
}

func main() {
    println(min(8, 10, 200))

    var x = []int{4, 2, 100}
    println(min(x...))
}
