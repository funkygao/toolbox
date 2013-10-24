package main

import "fmt"

// 变参函数
func printf(str string, args ...interface{}) (int, error) {
    _, err := fmt.Printf(str, args...)
    return len(args), err
}

func main() {
    count := 1
    closure := func(msg string) {
        printf("%s, %d\n", msg, count)
        count ++
    }

    closure("we are")
    closure("here and there")
}


