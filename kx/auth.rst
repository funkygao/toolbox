==============
authentication
==============

:Author: Gao Peng <funky.gao@gmail.com>
:Description: 
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::


SRP
===

http://srp.stanford.edu/design.html

js
--

register
^^^^^^^^

::
    
    srp = new SRP();
    srp.register();

        -> handshake(username)
        <- salt
        -> send_verifier(verifier)

login
^^^^^

::

    srp = new SRP();
    srp.identify();

        -> handshake(username, A)
        <- salt, B
        -> confirm_authentication(M)


Weak Authentication
-------------------

- plaintext password

- encoded password

  e,g HTTP Basic authentication

  ::

        client request:
            s := username + ":" + password
            r.Header.Set("Authorization", "Basic "+base64.StdEncoding.EncodeToString([]byte(s)))

        server:
            

- challange-response authentication

  User recv C, responds with f(C, P)

认证入口
=================
nginx


POST https://security.kaixin001.com/login/login_auth.php

Form data:

email: funky.gao@163.com

password: xxxxxx


POST POST https://security.kaixin001.com/login/login_probe.php


API
===

::

    cuser.getUidByEmail

    validatePwd
        DCredential_KxiApi
