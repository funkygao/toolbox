==============
ID Generator
==============

:Author: Gao Peng <funky.gao@gmail.com>
:Description: 
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::


::

    CREATE TABLE `idgenerator` (
        `kind` varchar(64) NOT NULL,
        `timed` tinyint(1) NOT NULL,
        `last_id` bigint(20) NOT NULL,
        `mtime` timestamp NOT NULL default '0000-00-00 00:00:00' on update CURRENT_TIMESTAMP,
        PRIMARY KEY  (`kind`)
    ) ENGINE=MyISAM DEFAULT CHARSET=latin1 
