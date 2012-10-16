package main

import "fmt"

type ByteSize float64

func (b ByteSize) String() string {
    switch {
    case b >= EB:
        return fmt.Sprintf("%.2fEB", b/EB)
    case b >= PB:
        return fmt.Sprintf("%.2fPB", b/PB)
    case b >= TB:
        return fmt.Sprintf("%.2fTB", b/TB)
    case b >= GB:
        return fmt.Sprintf("%.2fGB", b/GB)
    case b >= MB:
        return fmt.Sprintf("%.2fMB", b/MB)
    case b >= KB:
        return fmt.Sprintf("%.2fEB", b/KB)
    }

    return fmt.Sprintf("%.2fB", b)
}

const (
    _ = iota
    KB ByteSize = 1 << (10 * iota)
    MB
    GB
    TB
    PB
    EB
)

func main() {
    // show ... usage
    x := []int{1, 2, 3}
    y := []int{4, 5, 6}
    x = append(x, y...)
    fmt.Println(x)
    fmt.Println(KB, MB, GB, TB, PB)
    var b ByteSize = 12121212212
    fmt.Println(b)
}
