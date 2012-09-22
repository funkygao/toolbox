===========
go language
===========

:Author: Gao Peng <funky.gao@gmail.com>
:Description: basic go language programming
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

Command
=======

::

    go build my.go

    go run my.go

    go doc builtin

    godoc fmt Println

    godoc -http=":6060"


Features
========

Syntax
------

- no unused variable except '_'

- multiple return value

- type infer

- 类型后置

  var foo int


Builtin func
------------

- close

  关闭chan

- new

  用于各种类型的内存分配

  new(T) allocates zeroed storage for a new item of type T and returns its address, a value of type `*T`

  ::

        p := new(SyncedBuffer) // type *SyncedBuffer
        var p SyncedBuffer     // type SyncedBuffer

- make

  用于内建类型的内存分配，仅用于slice, map, channel

  it returns an initialized (not zeroed) value of type T (not `*T`)

  ::

        var v []int = make([]int, 100) // the slice v now refers to a new array of 100 ints

- delete

  on map

- copy

  copy slice

- append

  Append the elements to the end of the slice and return the result


- panic

  recover

- println

  print

- len


defer
-----

::

    f, _ = os.Open(filename)
    defer f.close()


recover
-------

::

    str := recover()


goroutine
---------
It originates in Hoare's Communicating Sequential Processes (CSP), it can also be seen as a type-safe generalization of Unix pipes.

It is a function executing concurrently with other goroutines in the same address space. 

It is lightweight, costing little more than the allocation of stack space. 
And the stacks start small, so they are cheap, and grow by allocating (and freeing) heap storage as required.

Goroutines are multiplexed onto multiple OS threads.

::

    go myfunc() // similar to the Unix shell's & notation for running a command in the background

    go func(delay int) {
        time.Sleep(delay)
        fmt.Println(msg)
    }(10)


chan
^^^^

::

    var c chan string = make(chan string)

    // send
    c <- "ping"

    // recv
    msg := <- c

GC
--

Simple mark-and-sweep collector

runtime is like JVM whose reposibilities includes:

- memory allocation

- gc

- stack handling

- goroutines

- channels

- reflection

- slice, map

- etc

Missing
-------

- assertions

- dynamic lib

- immutable var

- exceptions 


Usage
=====

分组
--------

::

    import (
        "fmt"
        "os"
    )

    const (
        PI = 3.14
        PREFIX = "go_"
    )


Redeclaration
-------------

::

    // valid
    a, b := 1, 2
    a, c : = 1, 5

    // invalid
    a, b := 1, 2
    a, b := 1, 5

If
--

::

    // valid
    if a := 1; a < 10 {
        println("ok")
    }

Cases
=====

- google map
