package main

import "fmt"

func main() {
    demoArray()
    demoNestedArray()
    demoMap()
    x, y := demoFunc(8, "go")
    println(x, y)
}

func demoArray() {
    var arr [10]int // 数组是不能变长的
    arr[0], arr[1] = 6, 9
    fmt.Printf("%d, %d, len=%d\n", arr[0], arr[1], len(arr))

    foo := [3]int{1, 2, 3}
    fmt.Println(foo)

    bar := [...]string{"we", "are", "here"} // ... 表示省略长度，自动计算
    fmt.Println(bar)
}

func demoNestedArray() {
    var arr [10][5]int
    foo := [2][3]int {[3]int{2, 3, 4}, [3]int{7,8,9}}

    fmt.Println(arr, foo)
}

func demoMap() {
    var users map[int] string
    users = make(map[int]string)
    users[1] = "gaopeng"
    users[8] = "liangling"
    fmt.Println(users, len(users))

    delete(users, 1)
    fmt.Println(users, len(users))
}

func demoFunc(x int, y string) (string, int) {
    return "we", 3
}
