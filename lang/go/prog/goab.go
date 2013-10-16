package main

import (
    vegeta "github.com/tsenart/vegeta/lib"
    "time"
    "flag"
    "fmt"
    "strings"
)

func main() {
    rps := flag.Uint64("r", 100, "rate: request per second")
    duration := flag.Int64("t", 5, "duration in seconds")
    flag.Parse()
    args := flag.Args()
    if len(args) == 0 {
        fmt.Println("goab [options] url")
        flag.Usage()
        return
    }

    cmd := "GET " + args[len(args)-1]
    fmt.Printf("Latency for [%s]\n%s\n", cmd, strings.Repeat("-", 40))

    targets, _ := vegeta.NewTargets([]string{cmd})
    results := vegeta.Attack(targets, *rps, time.Second * time.Duration(*duration))
    metrics := vegeta.NewMetrics(results)

    fmt.Printf("%8s: %s\n", "mean", metrics.Latencies.Mean)
    fmt.Printf("%8s: %s\n", "max", metrics.Latencies.Max)
    fmt.Printf("%8s: %s\n", "95%", metrics.Latencies.P95)
    fmt.Printf("%8s: %s\n", "99%", metrics.Latencies.P99)
}
