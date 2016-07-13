package main

import (
	"encoding/json"
	"fmt"
	"time"
)

func sliceIsByReference() {
	f := func(a []int) {
		fmt.Println("update a[0] to 1")
		a[0] = 1
	}

	a := []int{0}
	fmt.Println(a)
	f(a)
	fmt.Println(a, "so you see: slice is inline updated")
}

func recvFromClosedChanIsSafe() {
	ch := make(chan struct{})
	close(ch)
	t0 := time.Now()
	<-ch
	fmt.Printf("receive on closed channel is safe: returns after %s\n", time.Since(t0))
}

func nilChannel() {
	var ch chan struct{} = nil
	select {
	case <-ch:
		fmt.Println("got msg from nil channel")

	case ch <- struct{}{}:
		fmt.Println("sent msg to nil channel")

	case <-time.After(time.Second):
		fmt.Println("send and receive on nil channel blocks forever")

	}
}

func jsonDecodeNumberAlwaysFloat64() {
	var data = []byte(`{"status": 200}`)
	var result map[string]interface{}
	json.Unmarshal(data, &result)
	_, ok := result["status"].(int)
	if ok {
		fmt.Println("OH, golang changed? this should never happen")
	}

	fmt.Printf("%#T\n", result["status"])
	_, ok = result["status"].(float64)
	if ok {
		fmt.Println("Go treats numeric values in JSON as float64 numbers when you decode/unmarshal JSON data into an interface")
	}
}

func changeMapWhileRange() {
	m := map[string]struct{}{
		"a": struct{}{},
		"b": struct{}{},
	}
	for k, _ := range m {
		delete(m, "b")
		fmt.Println(k)
	}
}

func main() {
	sliceIsByReference()
	fmt.Println()

	recvFromClosedChanIsSafe()
	fmt.Println()

	nilChannel()
	fmt.Println()

	jsonDecodeNumberAlwaysFloat64()
	fmt.Println()

	changeMapWhileRange()
	fmt.Println()

}
