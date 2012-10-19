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

    go run -x my.go

    go doc builtin

    godoc fmt Println

    godoc -http=":6060"

    go list ./... # ”./...”表示当前目录（”./”）下的所有包（”...”)

    go test -v ./...


Features
========

Syntax
------

- no unused variable except '_'

- multiple return value

- type infer

- 类型后置

  var foo int

- pass by value

  not by reference

- 接口是由使用方按需定义
  
  而不用事前规划


Stack vs heap
-------------

消除了堆与栈的边界，Go 语言里面你不需要关心，也并不清楚，变量在堆上还是栈上

runtime自动选择何时使用stack，何时使用heap

go语言中使用的是非连续栈，原因是需要支持goroutine


Access control
--------------

at the package level

import
------

A Go program or package’s imports are first searched for under the GOPATH path or paths, and then under GOROOT


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

  make() always returns a reference to the value it created

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

conversion
----------

::

    a := 4.5
    b := int(a)


goroutine
---------
- 起源于Hoare's Communicating Sequential Processes (CSP)
  
  it can also be seen as a type-safe generalization of Unix pipes.

- 运行在同个地址空间

- lightweight
  
  they are created with 4K memory stack-space on the heap. 可以轻松地创建10万级别的goroutines

  他们使用segmented stack，自动地动态增加／减少内存使用。

  他们使用的stack不会被gc，而是当该goroutine退出后立即自动释放

- gc vs gccgo

  只有gc compiler会自动为goroutine分配线程，而gccgo只是为每个goroutine分配一个线程


::

    go myfunc() // similar to the Unix shell's & notation for running a command in the background

    go func(delay int) {
        time.Sleep(delay)
        fmt.Println(msg)
    }(10)

    func myfunc() {
        // xxx
        runtime.Gosched() // yield the processor without suspend the current goroutine
        // xxx
    }


channel
^^^^^^^

FIFO and preserve the order of items that are sent into them

The very act of communication through a channel guarantees synchronization.

Only one goroutine has access to a data item at any given time: so data races cannot occur, by design

Channel send and recv operations are atomic!

为了易读，channel的变量通常以ch或chan开头

- unbuffered

  send/recv block until the other side is ready
  
  the communication succeeds only when both sender and recver are ready

- buffered

  ch := make(chan int, 20)
  cap(ch) // 20, capability



::

    var c chan string = make(chan string)

    // send
    c <- "ping"

    // recv
    msg := <- c

    chanOfChans := make(chan chan int)


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


Performance
-----------

- vs c++

  20% slower than c++

- vs java and scala

  twice as fast and requiring 70% less memory

- vs python

  on average 25 x faster than Python 3, uses 1/3 of the memory

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

适用于import, const, var, type

::

    import (
        fm "fmt"
        "os"
    )

    const (
        PI = 3.14
        PREFIX = "go_"
    )

    const (
        Sunday = iota
        Monday
        Tuesday
    )

    type Color int
    const (
        Red Color = iota // 0
        Blue             // 1
        Green
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


File Structure
--------------

::

    package main

    import (
        "fmt"
    )

    const c = "C"

    var v int = 5

    type T struct {
    }

    func init() {
    }

    func main() {
    }

    func (t T)Method1() {
    }


main
----

When the function main() returns, the program exits: 
it does not wait for other (non-main) goroutines to complete.



Func
----

- func

- method

  - Has receiver

  - Every method name must be unique for any given type

    不支持java里的同名但参数不同的形式


Internals
=========

startup
-------

::

        runtime.osinit
            |
        runtime.schedinit 
            |
        runtime.newproc 
            |
        runtime.mstart 
            |
        schedule 
            |
        runtime.main 
            |
        main.main

Cases
=====

- google map

Remarks
=======

- init() is per file instead of per package
