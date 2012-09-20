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

- make

  用于内建类型的内存分配

- delete

  on map

- copy

  copy slice

- append

  append to slice

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

::

    go myfunc()


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
