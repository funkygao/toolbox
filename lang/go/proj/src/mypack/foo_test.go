package mypack

import "testing"

func TestFoo(t *testing.T) {
    t.Errorf("output 3, expected %d\n", 1)
}
