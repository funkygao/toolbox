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
	dataSize   int
	host       string
	port       string
	timeout    = time.Second * 10
	interval   = time.Millisecond * 20
)

func main() {
	var c int
	flag.StringVar(&host, "h", "54.184.78.104", "host")
	flag.StringVar(&port, "p", "11211", "port")
	flag.IntVar(&dataSize, "l", 1024, "cache value size in bytes")
	flag.IntVar(&c, "c", 2000, "concurrent conn")
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
	for i := 0; i < c; i++ {
		//time.Sleep(interval)
		go func() {
			for {
				mc := memcache.New(mcServer)
				mc.Timeout = timeout
				atomic.AddInt64(&concurrent, 1)
				for {
					_, err := mc.Get("foo")
					atomic.AddInt64(&totalnum, 1)
					if err != nil {
						atomic.AddInt64(&errnum, 1)
						fmt.Printf("%s\n", err)
						break
					}
				}

				atomic.AddInt64(&concurrent, -1)
			}

		}()
	}

	for i := 0; i < 260; i++ {
		atomic.LoadInt64(&concurrent)
		fmt.Printf("%v\n ", concurrent)
		time.Sleep(time.Microsecond * 70000)
	}

	fmt.Println(totalnum, errnum, 100.*float64(errnum)/float64(totalnum))

}
