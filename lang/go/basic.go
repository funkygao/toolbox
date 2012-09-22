package main

import (
    "fmt"
    "os"
    "reflect"
)

func main() {
    demoIf("if")
    demoSwitch("switch")
    demoArray("array")
    demoNestedArray("nested array")
    demoMap("map")
    demoOs("os package")
    demoAppend("append")
    demoChannel("channel")
    x, y := demoFunc(8, "go", "func")
    println(x, y)
    demoDebug("debug")
    demoFuncAsParam("func as param")
    demoReflect("reflect")
}

func demoReflect(tag string) {
    printDemoFeature(tag)

    x, y := 5, "Hello"
    println(reflect.TypeOf(x), reflect.TypeOf(y))
    fmt.Println(reflect.TypeOf(x))

    v := reflect.ValueOf(x)
    fmt.Println(v.Type(), v.Kind(), v.Interface())
}


func foo() {println("foo")}
func bar() {println("bar")}

func callFuncAsParam(f func()) {
    f()
}

func demoFuncAsParam(tag string) {
    printDemoFeature(tag)

    callFuncAsParam(foo)
}

func demoDebug(tag string) {
    printDemoFeature(tag)

    type X struct {
        x, y int
        z string
    }

    x := X{1, 3, "haha"}
    fmt.Printf("%+v, %#v, %T\n", x, x, x)
}

func demoChannel(tag string) {
    printDemoFeature(tag)

    c := make(chan int)
    go func() {
        s := 0
        for i:=0;i<2000000000;i++ {
            s ++
        }
        println(s)

        c <- 1 // Send a signal, value does not matter
    }()

    <- c
}

func demoAppend(tag string) {
    printDemoFeature(tag)

    x := []int{1, 5, 8}
    x = append(x, 4, 5, 6)
    fmt.Println(x)
}

func printDemoFeature(tag string) {
    println("\n\n", "Demo of", tag)
    for i := 0; i < 40; i++ {
        print("-")
    }
    println("\n")
}

func demoOs(tag string) {
    printDemoFeature(tag)

    fmt.Fprint(os.Stdout, "demoOs, haha ", 12, "\n")
    fmt.Println(fmt.Sprintf("%d is > %d\n", 5, 2))
}

func demoIf(tag string) {
    printDemoFeature(tag)

    if x := 5; x < 10 {
        println("If demo")
    }
}

func demoSwitch(tag string) {
    printDemoFeature(tag)

    n := 10
    switch n {
    case 1, 5, 11:
        println("oh")
        break
    case 4, 10:
        println("omg")
        break
    }

    switch {
    case n < 5:
        println(n, "<5")
        break
    case n >= 5:
        println(n, ">=5")
        break
    }
}

func demoArray(tag string) {
    printDemoFeature(tag)

    var arr [10]int // 数组是不能变长的
    arr[0], arr[1] = 6, 9
    fmt.Printf("%d, %d, len=%d\n", arr[0], arr[1], len(arr))

    foo := [3]int{1, 2, 3}
    fmt.Println(foo)

    bar := [...]string{"we", "are", "here"} // ... 表示省略长度，自动计算
    fmt.Println(bar)
}

func demoNestedArray(tag string) {
    printDemoFeature(tag)

    var arr [10][5]int
    foo := [2][3]int {[3]int{2, 3, 4}, [3]int{7,8,9}}

    fmt.Println(arr, foo)
}

func demoMap(tag string) {
    printDemoFeature(tag)

    var users map[int] string
    users = make(map[int]string)
    users[1] = "gaopeng"
    users[8] = "liangling"
    fmt.Println(users, len(users))

    delete(users, 1)
    fmt.Println(users, len(users))
}

func demoFunc(x int, y string, tag string) (string, int) {
    printDemoFeature(tag)

    return "we", 3
}

func init() {
    println("=============\ninit called\n=============")
}

