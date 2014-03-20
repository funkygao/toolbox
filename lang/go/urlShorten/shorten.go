package main

import (
	"crypto/rand"
	"fmt"
	"os"
)

const (
	alphanum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	urlLen   = 8
)

var (
	collisionCheckContainer = make(map[string]bool)
)

// just generate random string, nothing to do with param: url
func urlShortened(url string) string {
	alphanum := "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	bytes := make([]byte, 8) // shortend url length=8
	rand.Read(bytes)
	for i, b := range bytes {
		bytes[i] = alphanum[b%byte(len(alphanum))]
	}
	return string(bytes)
}

func main() {
	url := urlShortened(os.Args[1])
	fmt.Println(url)

	i := 0
	for {
		url := urlShortened(os.Args[1])
		if _, collision := collisionCheckContainer[url]; collision {
			fmt.Printf("Collision at %d\n", i)
			return
		}

		collisionCheckContainer[url] = true
		i++
	}
}
