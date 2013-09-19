=========================
mongodb
=========================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: NA
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

replica set
============

usage
-----

::

    >rs.initialize(config_rs);
    >rs.status();
    >rs.isMaster();

    >use local
    >db.oplog.rs.find()
    >db.printReplicationInfo()

