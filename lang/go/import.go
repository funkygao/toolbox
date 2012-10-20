package main

import (
    . "runtime" // use pkg without qualifying pkg name
    _ "os" // pkkg is imported for its side-effect only: call init() and global var initialized
)

func main() {
    println(NumCPU())
}
