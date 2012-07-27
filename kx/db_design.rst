=======================
一些设计细节
=======================

:Author: Gao Peng <funky.gao@gmail.com>

.. contents:: Table Of Contents
.. section-numbering::


用户信息表的设计
==========================

- s_user_property_0

  用户属性表：好友数/活跃度/内容贡献度/是否马甲/最后来访时间等

- s_user_info_0

  用户基本信息表：姓名/性别/昵称/出生地/现住地/性别/头像版本等

- s_user_logo_0

  头像信息表

- s_user_logo_history_0

  用户头像更新历史表

- s_user_pinfo_0

  用户密码信息表

- s_user_phistory_0

  用户密码修改历史

- s_user_paypinfo_0

  用户支付密码信息表

- s_user_payphistory_0
  
  用户支付密码修改历史

- s_user_pwd_question_0

  用户密码问题以及答案表

- s_user_moreinfo_0

  用户基本信息表，变化不频繁：真实姓名/注册时间/体型/喜欢的图书/偶像/个人介绍/邮编/电话/手机/QQ等

- s_user_exinfo_0

  户基本信息表，变化频繁：登录时间/短消息数/系统信息数/用户自己经常设置的项目等

- s_user_reginfo_0

  用户注册信息：注册来源/已经进入到第几步骤/完成注册的时刻

- s_userinfo_modify_record

  用户信息修改表

- s_user_regip_0

  用户注册 IP 表

- s_user_mayknown_0

  用户可能认识的人

- s_user_login_YYMMDD

  用户登录记录，每天一个表，用来统计活跃用户信息

- s_ip_login_YYMMDD

  IP登录记录,每天一个表

- s_user_login_record_0

  登录记录, 最多三次左右就可以了


好友关系表的设计
=====================

好友关系是单向的, 如果A把B加为自己的好友，则我们说B是A的'偶像', A是B的'粉丝'

- s_user_friend_mine_0

  用户的所有偶像，好友所属的组集合, 各组名之间用','分割

- s_user_friend_fan_0

  粉丝表(反向好友关系)


留脚印
==========

::

    CREATE TABLE s_user_visitor_0 (
        uid int NOT NULL default '0' COMMENT 'SPLIT_KEY',
        total int NOT NULL default 0, -- 总的访问人次
        mtime timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
        data blob NOT NULL default '', -- 最近去访的N个用户及时间，每个用户8位
        UNIQUE KEY(`uid`)
    )

    data = struct VisitTime {
        int uid;    // 用户ID
        int vtime;  // 访问时间
    } data[NUM];

此外，每个组件都有自己的单独表来保存脚印信息。e.g
s_user_home_visitor_0, s_user_diary_visitor_0, s_user_photo_visitor_0, etc



好友是否在线
==================

给定array of uids，走中间层

用户登录时，renewTime。如果用户有动作，则按时(比如每1分钟)更新表中的updateTime字段, 
如果updateTime与当前时间相差较大(比如10分钟)，则可认为该用户不在线。

updateTime太老的记录定时从表中删除以减小表的占用空间

::

    CREATE TABLE s_user_online (
        uid int NOT NULL default '0',
        logo int NOT NULL default '0',
        gender tinyint(2) NOT NULL default '0',
        birthday date NOT NULL default '0000-00-00',
        city varchar(64) NOT NULL default '',
        privacy1 int(11) NOT NULL default '0',
        privacy2 int(11) NOT NULL default '0',
        updateTime timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
        PRIMARY KEY(uid),
        INDEX(updateTime)
    )


机器人
============

cron with exclusive lock

它们真的有点像真的用户：

- 定期去外站抓图片／博客／新闻等

- 转好友的UGC

- 自己会定期更换头像


互动类型

- 请求加好友

- 送礼物

- 动他

- 转帖

- 投票

- and more...



定时job
=============

- CDN速度监测

- 监测iphone push

  /usr/local/nagios/libexec/check_tcp -H gateway.push.apple.com -p 2195 -t 5

- 监测php error log

- disk monitor

- mc monitor

- mysql monitor


拼音转汉字
=============


Push Server
===========

PServer 中间层

- push to mobile


- push to web

  
