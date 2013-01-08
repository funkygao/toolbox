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

COOKIE['_user']  => uid

- 注册新帐号::
    1                                       <-

    DReg_Func::regUser(params) {
        check(ip)
        get uid from idman
        insert into s_user_info(account)    <-
        insert into s_login_ex              <- 双写到 (s_accounts, s_user_accounts)
        s_user_moreinfo(passwd)             <-
        CUserRegister::addUserRegInfo
    }

    为了隔离数据库?
    为了方便调用?

    => createAccount {account^%S; passwd^%S}
    <= {uid^%i}

- 给已有uid绑定一个新帐号::
    1                                       <-

    DSecurity_Email_Control::c_chgEmail(params) {
        s_user_moreinfo.newemail
        insert into s_emailinfo
        send notification to old account    <-
    }
    
    需要实现如上所有逻辑?

    => bindAccount {uid^%i; account^%S}
    <= {ok^%b}

- 帐号密码认证::
    45                                      <-

    DCredential_KxiApi::validatePwd(uid, pwd)

    登录后，session里存uid or account?
    pwd目前在s_user_info里，换地方?
    
    => validateAccountPasswd {account^%S; passwd^%S}
    <= {ok^%b; ?uid^%i; ?session^%S}

- 基于帐号获取uid::

    CUser->getUidByEmail(email)
    s_login_ex
    
    => getUidByAccount {account^%S}
    <= {ok^%b; ?uid^%i}

- 获取基本注册信息::

    CUser

   => getUserRegistration {uid^%i}
   <= {ok^%b; realname^%S; gender^%S; birthday^%S; ctime^%S}

- 登录Session验证::
    
    => validateSession {session^%S}
    <= {ok^%b; ?uid^%i}

- 创建基本注册信息
- 更改基本注册信息

- 修改密码::

    DCredential_KxiApi::setPwd(uid, pwd, autocreate = true)

    => changeAccountPasswd {account^%S; oldpasswd^%S; newpasswd^%S}
    <= {ok^%b; ?uid^%i}
    
- 修改帐号::

    DSecurity_Email_Control::c_chgEmail(params)

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






>>> from kx.proxy import Delegate
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named proxy
>>> from kxi.proxy import Delegate
>>> p = Delegate('account@::9999')
>>> p.call('\0')
{'methods': ['create_account', 'delete_account', 'get_accounts', 'get_uid']}
>>> p.create_account(uid=54321, account='test123')
{'ok': True}
>>> p.create_account(uid=54321, account='test1236')
{'ok': True}
>>> p.get_accounts(uid=54321)
{'list': [['test123', '2013-01-08 12:41:17'], ['test1236', '2013-01-08 12:41:22']], 'ok': True}
>>> p.create_account(uid=5432, account='test123')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "build/bdist.linux-x86_64/egg/kxi/proxy.py", line 288, in wrap
  File "build/bdist.linux-x86_64/egg/kxi/proxy.py", line 281, in call
  File "build/bdist.linux-x86_64/egg/kxi/proxy.py", line 267, in request
  File "build/bdist.linux-x86_64/egg/kxi/proxy.py", line 259, in recv
kxi.proxy.Error: proxy.Error({'exception': 'MySQLdb::Error', 'code': 1062L, 'raiser': 'sQuery*DBMan @tcp:192.168.0.140:12321, sQuery*DBMan @tcp:127.0.0.1:9999, create_account*account @tcp:127.0.0.1:9999', 'message': "host=192.168.0.140:3309, mysql_error=Duplicate entry 'test123' for key 1", 'detail': {'what': "MySQLdb::Error(1062) at MySQLdb.cpp:325 --- host=192.168.0.140:3309, mysql_error=Duplicate entry 'test123' for key 1\nsql=INSERT INTO s_accounts_1 (`account`, `uid`) VALUES ('test123', '5432')", 'line': 325L, 'file': 'MySQLdb.cpp', 'calltrace': './DBManServer _ZN7MySQLdb5ErrorC1EPKciiRKSs\n./DBManServer _ZN7MySQLdb5queryEPKcmS1_PNS_9ResultExtE\n./DBManServer _ZN9SQueryJob4doitERK4XPtrI12DBConnectionE\n./DBManServer _ZN6DBTeam4workERK4XPtrI5DBJobEb\n./DBManServer _ZN9DBCluster9assignJobERK4XPtrI5DBJobE\n./DBManServer _ZN5DbMan12_kxi__sQueryERK4XPtrI6KQuestERKN3kxi7CurrentE\n./DBManServer _ZN3kxi22process_servant_methodEPNS_7ServantEPK9SymbolTabIMS0_F4XPtrI7KAnswerERKS3_I6KQuestERKNS_7CurrentEEES9_SC_\n./DBManServer _ZN3kxi8ServantI7processERK4XPtrI6KQuestERKNS_7CurrentE\n./DBManServer _ZN3kxi11ConnectionI12handle_questERNS_8CurrentIE\n./DBManServer _ZN3kxi12PtConnection7do_readERK4XPtrIN6XEvent10DispatcherEE\n./DBManServer _ZN3kxi12PtConnection11event_on_fdERK4XPtrIN6XEvent10DispatcherEEi\n./DBManServer _ZN6XEvent9EpollDisp4workEv\n./DBManServer [0x4a29b5]'}})
>>> p
<kxi.proxy.Delegate object at 0x2ab1bad7bd10>
>>> 
