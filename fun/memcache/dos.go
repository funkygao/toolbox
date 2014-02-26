package main

import (
	"flag"
	"fmt"
	"github.com/bradfitz/gomemcache/memcache"
	"runtime"
	"strings"
	"sync/atomic"
	"time"
)

var (
	concurrent int64
	errnum     int64
	totalnum   int64
	connnum    int64
	dataSize   int
	host       string
	loops      int
	show       bool
	port       string
	timeout    = time.Second * 10
	interval   = time.Millisecond * 20
)

func main() {
	var c int
	flag.StringVar(&host, "h", "54.184.78.104", "host")
	flag.StringVar(&port, "p", "11211", "port")
	flag.IntVar(&loops, "loop", 360, "loops count")
	flag.IntVar(&dataSize, "l", 1024, "cache value size in bytes")
	flag.IntVar(&c, "c", 2000, "concurrent conn")
	flag.BoolVar(&show, "progress", true, "show progress")
	flag.Parse()

	mcServer := host + ":" + port

	runtime.GOMAXPROCS(8)

	mc := memcache.New(mcServer)
	mc.Timeout = timeout

	if err := mc.Set(&memcache.Item{
		Key:   "foo",
		Value: []byte(strings.Repeat("X", dataSize))}); err != nil {
		panic(err)
	}

	t1 := time.Now()
	for i := 0; i < c; i++ {
		//time.Sleep(interval)
		go func() {
			for {
				mc := memcache.New(mcServer)
				atomic.AddInt64(&connnum, 1)
				mc.Timeout = timeout
				atomic.AddInt64(&concurrent, 1)
				for {
					_, err := mc.Get("foo")
					atomic.AddInt64(&totalnum, 1)
					if err != nil {
						atomic.AddInt64(&errnum, 1)
						if show {
							fmt.Printf("%s\n", err)
						}

						break
					}
				}

				atomic.AddInt64(&concurrent, -1)
			}

		}()
	}

	for i := 0; i < loops; i++ {
		atomic.LoadInt64(&concurrent)
		if show {
			fmt.Printf("%4d %v\n ", i+1, concurrent)
		}

		time.Sleep(time.Microsecond * 70000)
	}

	fmt.Printf("conn:%5d req:%9d %-6dreq/s err:%4d errRate:%.6f%%\n",
		connnum,
		totalnum, totalnum/int64(time.Since(t1).Seconds()),
		errnum, 100.*float64(errnum)/float64(totalnum))

}
