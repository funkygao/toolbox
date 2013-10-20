=========================
MMO game server
=========================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: NA
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

MMO vs HTTP
===========

- long conn vs short conn

- area based partition vs load balanced cluster

  地图的管理方式决定了我们的服务器结构

  同场景的玩家跑在一个进程内， 以达到最少的跨进程调用

- stateful vs stateless

- request/broadcast vs request/response

GameServer
==========

游戏服务器要处理的基本逻辑有

- move

- chat

- mission

- 技能

- 物品

- 生物

另外还有地图管理与消息广播来对其他高级功能做支撑，如纵队、好友、公会、战场和副本等


