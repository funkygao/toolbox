=========================
Fun+ Infrastructure
=========================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: NA
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

BigData
=======

key
---

::

    :rstory.source.key time() int_value
            ------
            fb_en

QA
==

th 2 memcached, get hit rate: 90/65


memcache set maybe fail

tcpdump -n 'tcp dst port 11211' -vvxXs 1500
tcpdump -n 'tcp port 11211' -vvxXs 1500
tcpdump -s 65535 -x -n -q -tttt port 11211


net.ipv4.tcp_fin_timeout = 60
net.ipv4.ip_local_port_range = 32768    61000
net.ipv4.tcp_tw_reuse = 0
net.ipv4.tcp_tw_recycle = 0

::

        mmc_prepare_key_ex  without warning
        mmc_get_pool        without warning
        php_var_serialize   Warning: Failed to serialize value
        mmc_pool_store      
            mmc_compress
            mmc_pool_find
            mmc_server_store

OPS
===

- server alarm

- mcenter.

- munin web only 1 host

- how git push to each web server

Gaming
======

- 角色扮演类

- 策略类

  更偏重于游戏的策略性和逻辑性，也就是考验游戏玩家的各种组合或搭配之类的游戏，对实时性的要求不会很高

- 混合类


LoC
===

- application

  18374

- system

  4258


OpenSource
==========

- aws
  CentOS

- supervisord

- munin/nagios

- chef

- mongodb

  mdadm raid0

- memcache

  memcache.hash_strategy="standard"
  memcache.hash_function="crc32"

- haproxy

- nginx/php-fpm

- syslog-ng

- postfix

- go

  mq consumer for pushing msg

- beanstalk

  mq engine

QA
==

- why both munin and nagios

- multiple role for a single aws instance?

- royal-flashlog.socialgamenet.com/loading.php?check=1930761&uid=1&step=1.x

- userguid

- banner

    https://banner-api.socialgamenet.com/loader.php?site=playroyalstory_it&wrap=royal-banner1
    https://banner-api.socialgamenet.com/loader.php?site=playroyalstory1_it&wrap=royal-inbox-hide-cont

::

    session  ttl=3 days, if age>1, refresh timestamp
    $_COOKIE['rs_session'] = f06d631388e78bcdfd83241f095bef7a0df6399c,1,1377824579
                             ======================================== = ==============
                                                                      uid request time
                             hash = sha1(self::$_sessionSecret.$sUserAgent);


Dataflow
========

::

    https://d3mxhpy50zysgx.cloudfront.net/v3/7622/main/it/Preloader.swf
    https://d3mxhpy50zysgx.cloudfront.net/v3/7470/loading/loading_it.swf
    https://d3mxhpy50zysgx.cloudfront.net/v3/7625/ver_it.amf
    https://d3mxhpy50zysgx.cloudfront.net/v3/7622/main/it/Main.swf

    https://royal-us.socialgamenet.com/time.php?key=13776744862160.19140625
    <= {"time":1377676554}

    d3mxhpy50zysgx.cloudfront.net/v3/game_config/it_US/171.amf
    gzip 1.8M to 490k

    https://royal-us.socialgamenet.com/persist/load_game_config/?key=13776735595050.80078125

    https://royal-us.socialgamenet.com/persist/load_user_data/?key=13776735595050.80078125
    Big json of user all data

    https://royal-us.socialgamenet.com/persist/batch/?key=13776735772420.66796875
    => commands=[{"params":{"power":0,"item":{"reward":{"Stone":1},"who":"self","action":"chopRock"},"guid":"27","ident":"Rock_3"},"opTime":1377676923,"action":"chop_growable"},{"params":{"positions":{"npcs":{"SmallTurtle":{"x":140,"y":79,"z":4}}}},"opTime":1377676923,"action":"update_positions"},{"params":{"flashLevel":2,"flashXp":118,"info":"batch","flashEnergy":25,"flashMaxEnergy":26},"opTime":1377676923,"action":"energyCheck"}]
    <= {"status":"OK","server_time":1377675846}

    https://royal-us.socialgamenet.com/loaddata/get_friend/?key=13776735626720.21875
    <= {"payload":{"world":{"friends_help":[]}},"status":"OK","server_time":1377675831}
    
    https://royal-us.socialgamenet.com/facebook/requests/?lang=it&_0.3168698470108211
    <= {"requestsNum":0,"gifts":[],"neighbors":[],"neighborsCount":-25,"helpRequests":[],"helpRequestsCount":-25,"reqArrId":[],"server_time":1377675842}

    https://api.facebook.com/method/fql.query?format=json&access%5Ftoken=CAABuBHFlEZBoBALmvpvupJYzMN5dv97qXtmZAVviCh0ZALQZAIUKkXe9HkhaExMK0ayVkvVOSQTBmwFcOLnEN63FcsMy7b2jVRbHYZAbwWcoCBsL5kgzM598U0VQgi9UV9uGH7bwgbHtPllGpDeFA5w7vTq0uZCQtdd9c4QuZAqawlPHUFkx7BYTglUCJ6cgQP0e7P1JeRFzQZDZD&query=SELECT%20uid%2C%20name%2C%20first%5Fname%2C%20last%5Fname%2C%20pic%5Fsquare%2C%20is%5Fapp%5Fuser%20FROM%20user%20WHERE%20uid%3Dme%28%29%20or%20uid%20in%20%28select%20uid2%20from%20friend%20where%20uid1%3Dme%28%29%29
    https://royal-us.socialgamenet.com/html/facebook/requests_loading.html?_=1377673560654


::

                         SslAcceleration+Compress
                         --------------------------
        DNSrr --------> | nginx (80|443)           |
                        | worker_connections 51200 |
                        |--------------------------|
                        | munin-node               |
                         --------------------------
                                |
                                | proxy_pass http://127.0.0.1:81
                                V
                         LoadBalance
                         ----------------------
                        | haproxy1.4.22 (81)   |
                        | maxconn 80000        |
                        |----------------------|
                        | munin-node           |
                        | nagios nrpe          |
                         ----------------------
                                |       |
                                |        -------                        
                                |               |                     AppServerFarm
                     ===========|===============|==============================================
                                | backend       | backend
                                V               V
                         -------------------   ...
                        | nginx(80|82?)     |
                        | access_log off    |
                        |-------------------|
                        | munin-node        |
                        | nagios nrpe       |
                        | postfix           |
                         -------------------
                                |
                                | fastcgi_pass 127.0.0.1:9000
                                V
                         ----------------------------
                        | fpm (9000)                 |
                        |----------------------------|
                        | /usr/local/php/lib/php.ini |
                        | memory_limit=128M          |
                        | max_execution_time=0       |
                        | eaccelerator.so            |
                        | memcache.so                |
                        | memcached.so               |
                        | mongo.so                   |
                         ----------------------------




Backend
============

::

                Logger  => als|local file
                GameLog => als+mongodb
                  |
        ------------------------
       |        ALS             |
       | (ApplicationLogSystem) |
        ------------------------


TODO
====

WebIM
-----

- jabber

  XMPP

- bosh

  Bidirectional-streams Over Synchronous HTTP

  XMPP XEP-0124

  http://www.iteye.com/topic/126428

Versions
========

- memcached

  1.4.5

- memcache.so

  2.2.6

- eAccelerator

  0.9.6.1

- mongo.so

  1.3.7


Publishment
===========

::

                  local work
        develop <------------> coding
          |
          |  http://royal-qa.socialgamenet.com/qa/index.html -> https://royal-qa.socialgamenet.com/
          V
        royal_th ===========> royal-th.socialgamenet.com
          |
          | 1-2 days latter
          V
        master
          ^
          | git pull
          |                 - royal-ae.socialgamenet.com
        royal_{locale}s => |- royal-de.socialgamenet.com
                           |- royal-fr.socialgamenet.com
                           |- royal-fr.socialgamenet.com
                           |- royal-nl.socialgamenet.com
                           |- royal-spil.socialgamenet.com
                            - royal-us.socialgamenet.com



        git co develop
        git pull [origin develop]
        git co -b f_xx develop
        do coding...committing...
        git co develop
        git merge --no-ff f_xx
        git push origin develop
        http://royal-qa.socialgamenet.com/qa/index.html

Schema
======

- user

  UserAccountModel

  ::

        ban




Memcache
========

=============================== ==================
key                             value
=============================== ==================
check_flash_time_{uid}          load_userdata time
=============================== ==================


::

        / (facebook/indexAction) => html & js
            |
            V
        persist/load_user_data => {batch_token:x, server_time:x, status:OK, payload:{}}
            |                     120k
            |
            V
        facebook/requests
            |
            V
        loaddata/get_friend
            |
            V
        persist/batch


git
===

::


                                    - cd /mnt/htdocs/qa
                                   |- assert(http://qa/up.sh was done) && assert(current branch is 'develop')
                                   |- git ca -m 'v'.svnNUM
        {qa}/mnt/htdocs/th.sh ===> |- git push
                 |                 |- git co royal_th;git pull;git merge --no-ff develop;git push
                 |                  - git co develop
                 |
        git co master; git merge --no-ff royal_th
                 |
                 |
                 |                    - cd /mnt/htdocs/qa
        {qa}/mnt/htdocs/publish.sh =>|- git co royal_us;git mg master;git push
                                     |- git co royal_fr;git mg master;git push
                                     |- ...
                                      - git co develop


index.php
=========

::


        {
            "accessToken": "CAABuBHFlEZBoBAP0U9Mqi7oNGkZAPVjryaQ3D5ZA0ujSZB5UTqZAZCC23elmfA8siieDjPe5iyxrcZAgskTk1d0tuuRZB2o7357Gyt5Likda3uQ7H9GV9p3xu0iCZBW5W75TsTC38KUAY0O52QwwZA9fCPSnVIfJrEIzBoVa71UiFhpT4lFmFIzoraQbbZBGaMBlD0ZD",
            "admin": 0,
            "amf": 1,
            "api_url": "https://royal-us.socialgamenet.com/",
            "app_id": "120965361374186",
            "app_name": "playroyalstory",
            "app_url": "http://apps.facebook.com/playroyalstory/",
            "bigData": "fb_en",
            "channelUrl": "https://royal-us.socialgamenet.com/html/channel.html",
            "email": "funky.gao@gmail.com",
            "flashVersion": 7741,
            "flushMain": 1,
            "guid": 10660866,
            "hashed_id": "sntpi-YUwi79HMrue2DgkkbymTxLyBlGQcMZXOqcgUGWJVA_Y",
            "img_url": "https://d3mxhpy50zysgx.cloudfront.net/v3/",
            "img_url2": "https://royal-us-asset.s3.amazonaws.com/v3/",
            "isHttps": 1,
            "isMonsterDebug": 0,
            "json_url": "https://d3mxhpy50zysgx.cloudfront.net/v3/game_config/en_US/196.amf",
            "language": "en",
            "loading_img": "https://d3mxhpy50zysgx.cloudfront.net/v3/img/loading/Loading_BacktoSchool.jpg",
            "loading_path": "https://d3mxhpy50zysgx.cloudfront.net/v3/7641/loading/loading_en.swf",
            "locale": "us",
            "log": 1,
            "log_url": "https://royal-flashlog.socialgamenet.com/l/us/",
            "main_path": "https://d3mxhpy50zysgx.cloudfront.net/v3/7741/main/en/Main.swf",
            "name": "\u9e4f",
            "payMod": 1,
            "payment": "true",
            "payment_id": "55",
            "pic_square": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/623555_100003391571259_1712659798_q.jpg",
            "pv": 1,
            "ref": "self",
            "res_json": "https://d3mxhpy50zysgx.cloudfront.net/v3/7690/main/en/loading.json",
            "royalStoryTest": 0,
            "secret": "070c8dcaf2185d2db0bac0afc8282228",
            "session_key": 1378699827,
            "showMask": 0,
            "startNow": 0,
            "statistic": "%7B%22loading%22%3A%221%22%7D",
            "timestamp": 1378899847,
            "tutorialStep": 0,
            "user_id": "100003391571259",
            "ver_game_config": 196,
            "versions_url": "https://d3mxhpy50zysgx.cloudfront.net/v3/7741/ver_en.amf"
        }




facebot
=======

::

        get http://www.facebook.com
            |
            | got signed_request and playroyalstory app info
            |
        post royal-us.socialgamenet.com
            |
            | got into flashvars.txt
            |





uid
===

for each request

::


        idmap::snsClassToUid
            |
        findByHashidOrSnsid
            |
            | not found
            |
        idSquenceModel::getNextValue('idmap')
            |
        update idmap for this uid



load_user_data

::

        useraccount::getUserAccount
            |
            | not exist
            |
        create all tables for this uid
