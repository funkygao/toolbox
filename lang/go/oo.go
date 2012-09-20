/*
 * Simulation of OO
 */
package main

import "fmt"

type Point struct {
    x, y int
}

func (p *Point) Get() (int, int) {
    return p.x, p.y
}

func (p *Point) Put(x, y int) {
    p.x, p.y = x, y
}

func (p *Point) add(x, y int) (int, int) {
    // by convention, non capital letter started method is private
    return p.x + x, p.y + y
}

type PointChild struct {
    Point // anonymous field
    z int
}

func (p *PointChild) Get() (int, int, int) {
    return p.x, p.y, p.z
}

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

