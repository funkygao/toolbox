package main

import (
    "github.com/howeyc/fsnotify"
    "fmt"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    fmt.Println("use inotify to monitor dir[s]")
    if len(os.Args) < 2 {
        fmt.Printf("Usage:\n\t%s dir [dir]\n", os.Args[0])
        return
    }

    exitCh := make(chan bool)
    signalCh := make(chan os.Signal, 1)
    go func() {
        <- signalCh
        exitCh <- true
    }()
    signal.Notify(signalCh, syscall.SIGINT, syscall.SIGTERM)

    watcher, err := fsnotify.NewWatcher()
    if err != nil {
        panic(err)
    }

    go onEvents(watcher)

    for _, dir := range os.Args[1:] {
        if err := watcher.Watch(dir); err != nil {
            panic(err)
        }
    }

    <- exitCh
    watcher.Close()
}

func onEvents(w *fsnotify.Watcher) {
    for {
        select {
        case event := <- w.Event:
            fmt.Println(event)
        case err := <- w.Error:
            fmt.Println("Error", err)
        }
    }
}
