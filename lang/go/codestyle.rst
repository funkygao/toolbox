=========================
GO coding style guide
=========================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: Go coding style
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::


Name
============

基本原则
------------
use mixedCaps or MixedCaps rather than underscore to write multiword names.

package name
------------

- 全小写

- 不用_分隔

- 就是目录名

constructor
-----------

创建foo.Foo实例的函数名称，应该是NewFoo

如果foo.Foo是该包的唯一的公开的struct，那么该构造函数名称可以简化为New

::

    foo := foo.NewFoo()

    foo := foo.New()

getter/setter
-------------

- getter

  ::

        type Foo struct {
            bar int
        }

        func (this *Foo) Bar() int { // not GetBar
            return this.bar
        }

        func (this *Foo) SetBar(bar int) {
            this.bar = bar
        }


interface
---------

以er结尾
