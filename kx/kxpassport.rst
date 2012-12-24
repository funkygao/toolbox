++++++++++++++++++++++++++++++++++++++++
           帐号中心功能设计
++++++++++++++++++++++++++++++++++++++++

-----------------------------
yangguang@corp.kaixin001.com
-----------------------------

:Author: 杨光

帐号核心功能
=========================
KXI接口
------------------
- 设置新帐号::

    => createAccount {account^%S; passwd^%S}
    <= {uid^%i}

- 给已有uid绑定一个新帐号::
    
    => bindAccount {uid^%i; account^%S}
    <= {ok^%b}

- 帐号密码认证::
    
    => validateAccountPasswd {account^%S; passwd^%S}
    <= {ok^%b; ?uid^%i; ?session^%S}

- 登录Session验证::
    
    => validateSession {session^%S}
    <= {ok^%b; ?uid^%i}

- 基于帐号获取uid::
    
    => getUserId {account^%S}
    <= {ok^%b; ?uid^%i}

- 获取基本注册信息::

   => getUserRegistration {uid^%i}
   <= {ok^%b; realname^%S; gender^%S; birthday^%S; ctime^%S}

- 创建基本注册信息
- 更改基本注册信息

- 修改密码::

    => changeAccountPasswd {account^%S; oldpasswd^%S; newpasswd^%S}
    <= {ok^%b; ?uid^%i}
    
- 修改帐号::

    => changeAccount {oldaccount^%S; newaccount^%S; passwd^%S}
    <= {ok^%b; ?uid^%i}

HTTP登录接口
---------------
部署在HTTPS下的登录接口
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
提供登录/验证码控制/用户封禁等功能
https://accounts.kaixin001.com/login/gateway
登录接口支持javascript封装调用

通用登录页面
~~~~~~~~~~~~~~~~~~~~~
标准化登录页面，支持有限定制化显示
https://accounts.kaixin001.com/login/landing
使用https form post登录, javascript free, 最可靠的方式



新增表
----------------
s_accounts
~~~~~~~~~~~~~~~
帐号表，按account分表，多个帐号可能会对应同一个uid

============= ================  =====================
   字段              类型             说明
============= ================  =====================
  account      varchar(128)       用户帐号(主键)
  uid          bigint             用户uid
  ctime        timestamp          创建时间
============= ================  =====================

s_user_accounts 
~~~~~~~~~~~~~~~~~~~~
按uid查询用户的一个或多个帐号 按uid分表

============= ================  =================
   字段              类型             说明
============= ================  =================
  uid          bigint             用户uid(索引)
  account      varchar(128)       用户帐号
  ctime        timestamp          创建时间
============= ================  =================

s_user_registration
~~~~~~~~~~~~~~~~~~~~~~~~~~
用户注册信息表，按uid分表，存储用户的基本注册信息

============= ================  =================
   字段              类型             说明
============= ================  =================
  uid          bigint             用户uid(主键)
  realname     varchar(128)       用户真名
  gender       bool               性别
  birthday     date               用户生日
  ctime        timestamp          创建时间
============= ================  =================



支付核心功能
============================
开心币功能
-------------
kxi接口, token验证，同时暴露到https上供http调用，每个token有自己的acl

- 消费开心币 spendBalance https://accounts.kaixin001.com/wallet/spend::
    
    => spendBalance {token^%S; uid^%i; amount^%S; environ^{%S^%X};}
    <= {ok^%b; balance^%i}

- 充值开心币 rechargeBalance https://accounts.kaixin001.com/wallet/recharge::
 
    => rechargeBalance {token^%S; uid^%i; amount^%S; environ^{%S^%X};}
    <= {ok^%b; balance^%i}
   
- 获取开心币余额 getBalance https://accounts.kaixin001.com/wallet/balance::
    
    => getBalance {token^%S; uid^%i; environ^{%S^%X};}
    <= {ok^%b; balance^%i}

- 获取开心币消费记录 getTransactions https://accounts.kaixin001.com/wallet/transactions::

    => getTransactions {token^%S; uid^%i; start^%i; end^%i]}
    <= {ok^%b; balance^%i; transactions^{fields^[%S]; rows[[%X]];}

支付功能
-------------
HTTP接口/网页形式出现, 通过各类支付手段充值到账户中的开心币，接口部署到 https://accounts.kaixin001.com/payment/ 下

- 支付网关，基于调用登录接口获取到的Session验证，用于处理支付需求并跳转到
  实际的支付页面
- 支付页面，用户选择支付方式和额度再跳转到具体支付方式的页面
- 支付完成页，支持跳转回请求来源

安全功能
============================
用户每次登录都需要记录到安全模块

- 密码重置
- 密保问题
- 手机绑定
- 异常登录控制
- 停用/删除帐号
  
开放平台帐号绑定
============================
TBD
