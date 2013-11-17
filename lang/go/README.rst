===========
go language
===========

:Author: Gao Peng <funky.gao@gmail.com>
:Description: basic go language programming
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::


注意事项
===============

method
------
不能为其他包和basic type来定义其方法

Command
=======

::

    go build my.go

    go run -x my.go

    godoc builtin

    godoc -http=":6060"

    go list ./... # ”./...”表示当前目录（”./”）下的所有包（”...”)

    go test -v ./...


Features
========

Syntax
------

- has no abstract class

- pass by value by default

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

there is no sub-packge, each package is a seperated package

import
------

A Go program or package’s imports are first searched for under the GOPATH path or paths, and then under GOROOT


Builtin func
------------

- new

  用于各种类型的内存分配

  new(T) allocates zeroed storage for a new item of type T and returns its address, a value of type `*T`

  ::

        p := new(SyncedBuffer) // type *SyncedBuffer
        var p SyncedBuffer     // type SyncedBuffer

- make

  用于内建类型的内存分配，仅用于
  
  - slice
    
  - map
    
  - channel

  make() always returns a reference to the value it created

  it returns an initialized (not zeroed) value of type T (not `*T`)

  ::

        var v []int = make([]int, 100) // the slice v now refers to a new array of 100 ints

- delete

  on map

- copy

  copy slice

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

Usage
=====

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


Remarks
=======

- init() is per file instead of per package

- selector

  In order to access the fields of a struct, whether the variable is of the 
  struct type or a pointer to the struct type, we use the same selector-notation

  ::

        var t1 MyStruct
        var t2 *MyStruct
        t1.i
        t2.i

- pipeline future

  ::

        func ParallelProcessData (in <- chan *Data, out <- chan *Data) {
            // make channels:
            preOut := make(chan *Data, 100)
            stepAOut := make(chan *Data, 100)
            stepBOut := make(chan *Data, 100)
            stepCOut := make(chan *Data, 100)

            // start parallel comutations
            go PreprocessData(in, preOut)
            go ProcessStepA(preOut, stepAOut)
            go ProcessStepB(stepAOut, stepBOut)
            go ProcessStepC(stepBOut, stepCOut)
            go PostProcessData(stepCOut, out)
        }


gdb
===

compile
-------

::

    go build -gcflags "-N -l"

init
----

~/.gdbinit

::

    source /opt/local/go/src/pkg/runtime/runtime-gdb.py

cmd
---

::

    info locals
    info args

    disas

    whatis variable

    b mypack.myfunc
    b 'regexp.(*Regexp).String'


Pitfall
=======

map is not thread safe
----------------------


GoogleAppEngine
===============

::

    cd /opt/app/google_appengine/demos
    dev_appserver.py helloworld/
