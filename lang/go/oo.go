/*
Simulation of OO

Here is the package comment.

Every package should have a package comment, a block comment preceding the package clause.

For multi-file packages, the package comment only needs to be present in one file, and any one will do.
*/
package main

import "fmt"

// Point stands for a location with x and y dimensions
type Point struct {
    x, y int
}

// Get the location of a Point.
// x and y is the return value.
func (p *Point) Get() (x int, y int) {
    return p.x, p.y
}

// Set the x,y dimension for Point.
func (p *Point) Put(x, y int) {
    p.x, p.y = x, y
}

func (p *Point) add(x, y int) (int, int) {
    // by convention, non capital letter started method is private
    return p.x + x, p.y + y
}

// Simulate OO inheritence.
type PointChild struct {
    Point // anonymous field
    z int
}

// Simulate OO override
func (p *PointChild) Get() (int, int, int) {
    return p.x, p.y, p.z
}

// An interface demo.
// Interface by duck type.
type Pointer interface {
    Get() (int, int)
    Put(x, y int)
}

func main() {
    p := Point{1, 3}
    fmt.Println(p.Get())
    x, y := p.add(1, 1)
    println(x, y)

    p1 := PointChild{p, 5}
    fmt.Println(p1.Get())
    fmt.Println(p1.x)

    var p2 Point
    p2.x, p2.y = 4, 5
    fmt.Println(p2)

    p3 := Point{x: 6, y: 9}
    fmt.Println(p3)
}

