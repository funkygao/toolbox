package main

import (
    "fmt"
    "sort"
)

type ByLength []string

// implement sort.Interface - Len, Swap, Less
func (s ByLength) Len() int {
    return len(s)
}

func (s ByLength) Swap(i, j int) {
    s[i], s[j] = s[j], s[i]
}

func (s ByLength) Less(i, j int) bool {
    return len(s[i]) < len(s[j])
}

func customizedSort() {
    strs := []string{"peach", "banana", "kiwi"}
    sort.Sort(ByLength(strs))
    fmt.Println(strs)
}

func main() {
    internalSort()
    customizedSort()
}

func internalSort() {
    strs := []string{"c", "a", "b"}
    sort.Strings(strs)  // inplace
    fmt.Println(strs)

    ints := []int{4, 2, 19, 22, 11}
    sort.Ints(ints)
    fmt.Println(ints)

    fmt.Println(sort.IntsAreSorted(ints))
}
