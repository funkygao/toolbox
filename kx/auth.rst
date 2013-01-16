==============
authentication
==============

:Author: Gao Peng <funky.gao@gmail.com>
:Description: 
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::


认证入口
=================
nginx


POST https://security.kaixin001.com/login/login_auth.php

Form data:

::

    email: funky.gao@163.com
    password: xxxxxx


POST https://security.kaixin001.com/login/login_probe.php


SSO
===

::

        after user login success
                |
            /login/check_cookie.php
                    |
            sign = genSSOSign(_uid, time(), remoteIp) 
                    |
            mc.set(_uid, (sign, _uid))
                    |
            <script src='/login/set_cookie.php?sign=$sign'></script>
                        |
                validate sign
                        |
                header("P3P: CP=CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR");
                        |
                setcookies



rememberMe
==========

::

        setRememberCookie
                |
            insert into s_user_persist_login(uid, series, token)
            verify = base64_encode($uid . ':' . $series . ':' . $token);  
            setcookie('_kx', verify, 1 year)


        getRememberCookie
                |
            getcookie('_kx')
            verify = renew_token()
                    |
                insert into s_user_persist_login(uid, series, token)
                |
            setcookie('_kx', verify, 1 year)
