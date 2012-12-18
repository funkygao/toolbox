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


`
+-------------------------------+-------+------------------+---------------------+
| city_requestid                |     0 |       2276440790 | 2012-12-06 14:16:17 | 
| city_hireid                   |     0 |        380769782 | 2012-12-06 14:16:17 | 
| city_helpid                   |     0 |      21639461906 | 2012-12-06 14:16:17 | 
| forwardid                     |     1 | 1420584105896810 | 2012-12-06 14:16:17 | 
| city_arrestid                 |     0 |       1418004090 | 2012-12-06 14:16:17 | 
| gchatmid                      |     0 |          9424279 | 2012-12-06 14:16:17 | 
| city_oilwellrequestid         |     0 |       2665622782 | 2012-12-06 14:16:17 | 
| city_cutid                    |     0 |       2651117066 | 2012-12-06 14:16:17 | 
| login_token                   |     0 |       8767377078 | 2012-12-06 14:16:17 | 
| city_aidrequestid             |     0 |        248475999 | 2012-12-06 14:16:17 | 
| photos_bqid                   |     1 | 1420584106392919 | 2012-12-06 14:16:17 | 
| sims_interaction_id           |     0 |         20332880 | 2012-12-06 14:16:17 | 
| sims_notice_id                |     0 |        400987046 | 2012-12-06 14:16:17 | 
| sims_message_id               |     0 |        474492532 | 2012-12-06 14:16:17 | 
| sims_giftlog_id               |     0 |        812558787 | 2012-12-06 14:16:17 | 
| sims_share_id                 |     0 |        166081533 | 2012-12-06 14:16:17 | 
| kx_pay_trace_id               |     0 |        153696553 | 2012-12-06 14:16:17 | 
| city_tradeid                  |     0 |          8503461 | 2012-12-06 14:16:17 | 
| kxc_c_notice                  |     0 |        142074067 | 2012-12-06 14:16:17 | 
| gamefriend_notice_id          |     0 |         27642609 | 2012-12-06 14:16:17 | 
| video_xid                     |     0 |         68150686 | 2012-12-06 14:16:17 | 
| usernewsid_121206             |     0 |          6615859 | 2012-12-06 14:16:17 | 
+-------------------------------+-------+------------------+---------------------+`
