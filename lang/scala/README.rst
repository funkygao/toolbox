===================
Scala demonstration
===================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: Scala is widely and wisely used in twitter
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

Syntax
======

Many classes have a companion object whose methods act just like static methods do in Java.

if (x>0) 1 else ()  // () is Unit(like void in Java)

Features
--------

- lazy values

  lazy val words = io.Source.fromFile("/usr/share/dict/words").mkString

Pattern Matching
----------------


Block Expression
----------------

::

    val distance = {val dx=x-x0; val dy=y-y0; math.sqrt(dx*dx+dy*dy)}


foreach
-------

::

    for (i <- 1 to 10) // make i traverse all values of the expression to the right of the <-
