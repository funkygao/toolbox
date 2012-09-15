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

    go run my.go

    godoc fmt Println

    godoc -http=":6060"


Features
========

Syntax
------

- no unused variable except '_'

- multiple return value

- type infer


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
