package main

import (
	"testing"
)

func BenchmarkUrlShortener(b *testing.B) {
	for i := 0; i < b.N; i++ {
		urlShortened("http://google.com")
	}
}
