=======================
一些常用算法
=======================

:Author: Gao Peng <funky.gao@gmail.com>

.. contents:: Table Of Contents
.. section-numbering::


CPM广告
===========


你可能会关注的好友
==========================

::

    从脚印里找出最近联系人
        |
    去掉非好友
        |
    去掉非好友
        |
    去掉已经特别关注的
        |
    批量取得userInfos(uids) -> shortname, icon, uid


好友推荐
================

::

    取得亲密度较高的好友uids
        |
    取得我他们的好友列表，其中每个uid里包含了我与他的共同好友uid
        |
    去掉黑名单
        |
    去掉已经加入的好友
        |
    去掉机构名人
