package main

import (
	"fmt"
	"runtime"
	"sync"
)

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())
	var wg sync.WaitGroup
	tube := make(chan int)

	// Dispatch loop
	for i := 0; i < 12345; i++ {
		wg.Add(1)

		// Worker
		go func(n int) {
			defer wg.Done()
			if n%3 != 0 {
				return
			}
			n = n * 2
			tube <- n
		}(i)
	}

	// Gatekeeper
	go func() {
		wg.Wait()
		close(tube)
	}()

	// Processing
	sum, count := 0, 0
	for v := range tube {
		sum += v
		count++
	}

	fmt.Println("Sum:", sum, "Numbers:", count, "Average:", float64(sum)/float64(count))
}
