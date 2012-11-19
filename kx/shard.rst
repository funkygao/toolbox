==============
ID Generator
==============

:Author: Gao Peng <funky.gao@gmail.com>
:Description: 
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

Routing
=======

mysql> desc kind_setting;

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

mysql> desc server_setting;

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

mysql> desc table_setting;

+---------+-------------+------+-----+---------+-------+
| Field   | Type        | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| kind    | varchar(64) | NO   | PRI | NULL    |       | 
| no      | int(11)     | NO   | PRI | NULL    |       | 
| sid     | int(11)     | NO   |     | NULL    |       | 
| db_name | varchar(64) | NO   |     | NULL    |       | 
+---------+-------------+------+-----+---------+-------+
