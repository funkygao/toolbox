++++++++++++++++++++++++++++++++++++++++
           �ʺ����Ĺ������
++++++++++++++++++++++++++++++++++++++++

-----------------------------
yangguang@corp.kaixin001.com
-----------------------------

:Author: ���

�ʺź��Ĺ���
=========================
KXI�ӿ�
------------------

COOKIE['_user']  => uid

- ע�����ʺ�::
    1                                       <-

    DReg_Func::regUser(params) {
        check(ip)
        get uid from idman
        insert into s_user_info(account)    <-
        insert into s_login_ex              <- ˫д�� (s_accounts, s_user_accounts)
        s_user_moreinfo(passwd)             <-
        CUserRegister::addUserRegInfo
    }

    Ϊ�˸������ݿ�?
    Ϊ�˷������?

    => createAccount {account^%S; passwd^%S}
    <= {uid^%i}

- ������uid��һ�����ʺ�::
    1                                       <-

    DSecurity_Email_Control::c_chgEmail(params) {
        s_user_moreinfo.newemail
        insert into s_emailinfo
        send notification to old account    <-
    }
    
    ��Ҫʵ�����������߼�?

    => bindAccount {uid^%i; account^%S}
    <= {ok^%b}

- �ʺ�������֤::
    45                                      <-

    DCredential_KxiApi::validatePwd(uid, pwd)

    ��¼��session���uid or account?
    pwdĿǰ��s_user_info����ط�?
    
    => validateAccountPasswd {account^%S; passwd^%S}
    <= {ok^%b; ?uid^%i; ?session^%S}

- �����ʺŻ�ȡuid::

    CUser->getUidByEmail(email)
    s_login_ex
    
    => getUidByAccount {account^%S}
    <= {ok^%b; ?uid^%i}

- ��ȡ����ע����Ϣ::

    CUser

   => getUserRegistration {uid^%i}
   <= {ok^%b; realname^%S; gender^%S; birthday^%S; ctime^%S}

- ��¼Session��֤::
    
    => validateSession {session^%S}
    <= {ok^%b; ?uid^%i}

- ��������ע����Ϣ
- ���Ļ���ע����Ϣ

- �޸�����::

    DCredential_KxiApi::setPwd(uid, pwd, autocreate = true)

    => changeAccountPasswd {account^%S; oldpasswd^%S; newpasswd^%S}
    <= {ok^%b; ?uid^%i}
    
- �޸��ʺ�::

    DSecurity_Email_Control::c_chgEmail(params)

    => changeAccount {oldaccount^%S; newaccount^%S; passwd^%S}
    <= {ok^%b; ?uid^%i}

HTTP��¼�ӿ�
---------------
������HTTPS�µĵ�¼�ӿ�
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
�ṩ��¼/��֤�����/�û�����ȹ���
https://accounts.kaixin001.com/login/gateway
��¼�ӿ�֧��javascript��װ����

ͨ�õ�¼ҳ��
~~~~~~~~~~~~~~~~~~~~~
��׼����¼ҳ�棬֧�����޶��ƻ���ʾ
https://accounts.kaixin001.com/login/landing
ʹ��https form post��¼, javascript free, ��ɿ��ķ�ʽ



������
----------------
s_accounts
~~~~~~~~~~~~~~~
�ʺű���account�ֱ�����ʺſ��ܻ��Ӧͬһ��uid

============= ================  =====================
   �ֶ�              ����             ˵��
============= ================  =====================
  account      varchar(128)       �û��ʺ�(����)
  uid          bigint             �û�uid
  ctime        timestamp          ����ʱ��
============= ================  =====================

s_user_accounts 
~~~~~~~~~~~~~~~~~~~~
��uid��ѯ�û���һ�������ʺ� ��uid�ֱ�

============= ================  =================
   �ֶ�              ����             ˵��
============= ================  =================
  uid          bigint             �û�uid(����)
  account      varchar(128)       �û��ʺ�
  ctime        timestamp          ����ʱ��
============= ================  =================

s_user_registration
~~~~~~~~~~~~~~~~~~~~~~~~~~
�û�ע����Ϣ����uid�ֱ��洢�û��Ļ���ע����Ϣ

============= ================  =================
   �ֶ�              ����             ˵��
============= ================  =================
  uid          bigint             �û�uid(����)
  realname     varchar(128)       �û�����
  gender       bool               �Ա�
  birthday     date               �û�����
  ctime        timestamp          ����ʱ��
============= ================  =================



֧�����Ĺ���
============================
���ıҹ���
-------------
kxi�ӿ�, token��֤��ͬʱ��¶��https�Ϲ�http���ã�ÿ��token���Լ���acl

- ���ѿ��ı� spendBalance https://accounts.kaixin001.com/wallet/spend::
    
    => spendBalance {token^%S; uid^%i; amount^%S; environ^{%S^%X};}
    <= {ok^%b; balance^%i}

- ��ֵ���ı� rechargeBalance https://accounts.kaixin001.com/wallet/recharge::
 
    => rechargeBalance {token^%S; uid^%i; amount^%S; environ^{%S^%X};}
    <= {ok^%b; balance^%i}
   
- ��ȡ���ı���� getBalance https://accounts.kaixin001.com/wallet/balance::
    
    => getBalance {token^%S; uid^%i; environ^{%S^%X};}
    <= {ok^%b; balance^%i}

- ��ȡ���ı����Ѽ�¼ getTransactions https://accounts.kaixin001.com/wallet/transactions::

    => getTransactions {token^%S; uid^%i; start^%i; end^%i]}
    <= {ok^%b; balance^%i; transactions^{fields^[%S]; rows[[%X]];}

֧������
-------------
HTTP�ӿ�/��ҳ��ʽ����, ͨ������֧���ֶγ�ֵ���˻��еĿ��ıң��ӿڲ��� https://accounts.kaixin001.com/payment/ ��

- ֧�����أ����ڵ��õ�¼�ӿڻ�ȡ����Session��֤�����ڴ���֧��������ת��
  ʵ�ʵ�֧��ҳ��
- ֧��ҳ�棬�û�ѡ��֧����ʽ�Ͷ������ת������֧����ʽ��ҳ��
- ֧�����ҳ��֧����ת��������Դ

��ȫ����
============================
�û�ÿ�ε�¼����Ҫ��¼����ȫģ��

- ��������
- �ܱ�����
- �ֻ���
- �쳣��¼����
- ͣ��/ɾ���ʺ�
  
����ƽ̨�ʺŰ�
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
