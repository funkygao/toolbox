package main

import (
    "fmt"
    "log"
    "strings"
    "os"
    "go/scanner"
)

type Partial struct {
    key, value string
}

type Result struct {
    token string
    counts map[string] int
}

// index a file
func Map(filename string, next chan Partial) {
    file, err := os.Open(filename)
    if err != nil {
        log.Fatal("failed open " + filename)
    }

    var s scanner.Scanner
    s.Init(file)
    token := s.Scan()
    for token != scanner.EOF {
        next <- Partial{s.TokenText(), filename}
        token = s.Scan()
    }

    next <- Partial{"", ""}
}

// reversed index
func Reduce(token string, files []string, final chan Result) {
    counts := make(map[string] int)
    for _, file := range files {
        counts[file] ++
    }

    final <- Result{token, counts}
}

func collectPartials(next chan Partial, count int, final chan map[string] map[string] int) {
    nexts := make(map[string] []string)
    for count > 0 {
        res := <- next
        if res.value == "" && res.key == "" {
            count --
        } else {
            v := nexts[res.key]
            if v == nil {
                v = make([]string, 0, 10)
            }
            v = append(v, res.value)
            nexts[res.key] = v
        }
    }

    collect := make(chan Result)
    for token, files := range nexts {
        go Reduce(token, files, collect)
    }

    results := make(map[string] map[string] int)
    for _, _ = range nexts {
        r := <- collect
        results[r.token] = r.counts
    }

    final <- results
}

func main() {
    next := make(chan Partial)
    final := make(chan map[string] map[string] int)
    dir, _ := os.Open(".")
    names, _ := dir.Readdirnames(-1)
    go collectPartials(next, len(names), final)

    for _, file := range names {
        if strings.HasPrefix(file, ".go") {
            go Map(file, next)
        } else {
            next <- Partial{"", ""}
        }
    }

    result := <- final

    for token, counts := range result {
        fmt.Printf("\n\nToken: %v\n", token)
        total := 0
        for file, count := range counts {
            fmt.Printf("\t%s: %d\n", file, count)
            total += count
        }
        fmt.Printf("Total: %d\n", total)
    }
}

