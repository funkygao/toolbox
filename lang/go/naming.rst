===================
Good naming examples
===================

:Author: Gao Peng <funky.gao@gmail.com>
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

设计
========

::

    Task
    Worker
    this.self

    type Pool struct {
        Mu sync.Mutex
        Tasks []Task
    }


变量
=========

::

    rbuf := bufio.NewReader(xxx)
    wbuf := bufio.NewWriter(xxx)

    rw, e := listener.Accept()

    v, present := m[key]
    v, found := m[key]

    expected, got

    t.Errorf("expected %d, got %d", expected, num)

类名
=======

type DefaultFoo struct {
}

type ConcreteFoo struct {
    DefaultFoo
}


文件名
=========

::

    schedule.go
    stats.go
    store.go
    protocol.go
    example_test.go
