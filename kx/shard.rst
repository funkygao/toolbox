==============
ID Generator
==============

:Author: Gao Peng <funky.gao@gmail.com>
:Description: 
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

Current
=======

Routining
---------

::

    (kind, split_key)
        |
        | lookup(kind)
        V
    kind_setting
        |
        | lookup(kind, no=split_key % table_num)
        V
    table_setting
        |
        | lookup(sid)
        V
    server_setting
        |
    (host, port, user, pass)


Mapping tables
--------------

kind_setting
^^^^^^^^^^^^

+--------------+-------------+------+-----+---------+-------+
| Field        | Type        | Null | Key | Default | Extra |
+--------------+-------------+------+-----+---------+-------+
| kind         | varchar(64) | NO   | PRI | NULL    |       | 
| table_num    | int(11)     | NO   |     | NULL    |       | 
| table_prefix | varchar(64) | NO   | UNI | NULL    |       | 
| id_field     | varchar(64) | NO   |     | NULL    |       | 
| remark       | text        | NO   |     | NULL    |       | 
| enable       | tinyint(1)  | NO   |     | 1       |       | 
+--------------+-------------+------+-----+---------+-------+

server_setting
^^^^^^^^^^^^^^

+-----------------+------------------+------+-----+---------+----------------+
| Field           | Type             | Null | Key | Default | Extra          |
+-----------------+------------------+------+-----+---------+----------------+
| sid             | int(11)          | NO   | PRI | NULL    | auto_increment | 
| master_sid      | int(11)          | NO   | MUL | NULL    |                | 
| host            | varchar(255)     | NO   | MUL | NULL    |                | 
| port            | int(10) unsigned | NO   |     | NULL    |                | 
| user            | varchar(32)      | NO   |     | NULL    |                | 
| passwd          | varchar(32)      | NO   |     | NULL    |                | 
| active          | tinyint(1)       | NO   |     | 1       |                | 
| remark          | text             | NO   |     | NULL    |                | 
| backup          | tinyint(1)       | NO   |     | 0       |                | 
| backup_priority | int(11)          | YES  |     | 99      |                | 
+-----------------+------------------+------+-----+---------+----------------+

table_setting
^^^^^^^^^^^^^

+---------+-------------+------+-----+---------+-------+
| Field   | Type        | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| kind    | varchar(64) | NO   | PRI | NULL    |       | 
| no      | int(11)     | NO   | PRI | NULL    |       | 
| sid     | int(11)     | NO   |     | NULL    |       | 
| db_name | varchar(64) | NO   |     | NULL    |       | 
+---------+-------------+------+-----+---------+-------+

Problem
-------

- hard to rebalance

  - can only scale up to 2**N shards

  - need 50% relocate data when N=1

  - has stop-the-world

- key not sorted


Enhancement
===========

::

    (s_user_info,     0, "user:pass@192.156.0.1:3367")
    (s_user_info, 15000, "user:pass@192.156.0.2:3368")
                  -----
                  startId


    regions are split in 2 at the middle key
