package main

import (
	"fmt"
	"math/rand"
	"runtime"
	"time"
)

func makeBuffer() []byte {
	return make([]byte, rand.Intn(5000000)+5000000)
}

func main() {
	pool := make([][]byte, 20)

	var m runtime.MemStats
	makes := 0
	for {
		b := makeBuffer()
		makes += 1
		i := rand.Intn(len(pool))
		pool[i] = b

		time.Sleep(time.Second)

		bytes := 0

		for i := 0; i < len(pool); i++ {
			if pool[i] != nil {
				bytes += len(pool[i])
			}
		}

		runtime.ReadMemStats(&m)
		if makes%18 == 0 {
			fmt.Printf("%12s %12s %12s %12s %8s %6s\n",
				"HeapSys", "bytes", "HeapAlloc", "HeapIdle",
				"HpRlse", "make")
		}

		fmt.Printf("%12d %12d %12d %12d %8d %6d\n",
			m.HeapSys, bytes, m.HeapAlloc,
			m.HeapIdle, m.HeapReleased, makes)
	}
}
