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
- �������ʺ�::

    => createAccount {account^%S; passwd^%S}
    <= {uid^%i}

- ������uid��һ�����ʺ�::
    
    => bindAccount {uid^%i; account^%S}
    <= {ok^%b}

- �ʺ�������֤::
    
    => validateAccountPasswd {account^%S; passwd^%S}
    <= {ok^%b; ?uid^%i; ?session^%S}

- ��¼Session��֤::
    
    => validateSession {session^%S}
    <= {ok^%b; ?uid^%i}

- �����ʺŻ�ȡuid::
    
    => getUserId {account^%S}
    <= {ok^%b; ?uid^%i}

- ��ȡ����ע����Ϣ::

   => getUserRegistration {uid^%i}
   <= {ok^%b; realname^%S; gender^%S; birthday^%S; ctime^%S}

- ��������ע����Ϣ
- ���Ļ���ע����Ϣ

- �޸�����::

    => changeAccountPasswd {account^%S; oldpasswd^%S; newpasswd^%S}
    <= {ok^%b; ?uid^%i}
    
- �޸��ʺ�::

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
