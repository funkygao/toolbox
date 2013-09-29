=========================
Ideas Make Big Change
=========================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: NA
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::


Ideas
=====

- 灰度发布

- A/B 测试

- Feature Flag

  紧急关闭一些特性，类似于graceful degrade

- php google analytics integration

  http://code.google.com/p/php-ga/

- how to add more memcached when dau is growing rapidly



web game

::


        web server
        task server
        db server(cache server)
    


ConfigFiles
===========

requirement
-----------

- do we need {if/loop/var}?

- need @extends

existing
--------

- YAML

- JSON

- ini

- xml

solutions
---------

- use sqlite3 as storage

  faster and use less mem

  gui for sqlite3

- vcl

  varnish configuration language

- puppet configuration language

  deprecate pupput ruby DSL

- lua

- https://code.google.com/p/coil/
