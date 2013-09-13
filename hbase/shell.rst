=========================
HBase shell usage
=========================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: NA
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

table
=====

- list

  show all tables

- describe '{table}'

- drop '{table}'

  disable '{table}'

- create '{table}' '{cf}'


data
====

- put

  put 'test', 'row1', 'cf:a', 'value1'

  put 'test', 'row2', 'cf:b', 'value2'

- scan

  scan 'test'

- get

  get 'blog','1',{COLUMN=>'author:name',VERSIONS=>2}

- delete

  - delete a column

    delete 'blog','1','author:name'

  - delete a whole rowkey

    deleteall 'blog','1'  


misc
====

- status

- version
