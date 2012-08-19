=========================
Mysql index best practice
=========================

:Author: Gao Peng <funky.gao@gmail.com>

.. contents:: Table Of Contents
.. section-numbering::


B+Tree
======

data stored in leaf nodes



MyISAM vs Innodb
================

MyISAM
------

Data pointers point to physical offset in the data file

All indexes are essentially equivalent

Innodb
------

Secondary indexes store primary key as data pointer


How Mysql uses indexes
======================

- data lookup

- sorting

- avoid reading data

- special optimizations


Cases
=====

- select * from players where country='cn' order by score desc limit 10

  index(country, score)

- select max(salary) from employee group by dept_id

  index(dept_id, salary)

  Using index for group-by

- select * from tbl where a=5 or b=6

  index(a), index(b) is better
  index(a, b) can't be used for this query


explain
=======

type
----

from 'good' to 'bad':

- system

- const

- rq_ref

- ref

- range

- index

- ALL


Join
====

Mysql performs joins as 'nested loops'

::

    select * from posts, comments where author='peter' and comments.post_id=posts.id

    Scan table 'posts' which have 'peter' as an author, then for every such post go to comments table to fetch all comments

- have all JOINs indexed

  This is very important


Covering index
==============

Reading index only and not accessing the data
